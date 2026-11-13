"""Client-ready driver charts for "which behaviours go with a bigger / more frequent outcome" models.

Every function takes a plain pandas DataFrame (the column contract is in each docstring and in README.md), draws
one figure, optionally saves it, and returns the matplotlib Figure. Nothing reads notebook globals, so the same
calls work for any outcome (AOV, frequency, spend, churn probability ...) and any two-segment comparison.

Conventions shared by every chart
    unit        ds_charts.Units("$", "per order") or Units("orders", "per year")
    segments    list of segment ids in display order; seg_labels maps id -> readable name
    verdict     "SHIP" (passed every gate) or anything else (held) - held levers are drawn grey
    effects     signed: > 0 = goes with a higher outcome (blue), < 0 = lower (red)
"""
from __future__ import annotations

import textwrap
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, PercentFormatter, StrMethodFormatter

from .style import PALETTE, SEGMENT_COLORS, DEFAULT_FOOTNOTE, Units, apply_style, clean_axes, footnote, save_fig

__all__ = ["effect_bars", "effect_bars_single", "ranking_bars", "marginal_curve", "marginal_curves",
           "importance_bars", "fit_bars", "gap_bars", "scorecard_table", "scorecard_figure", "segment_distributions"]


# ---------------------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------------------
def _seg_colors(segments: Sequence[str], seg_colors: dict | None) -> dict:
    return seg_colors or {s: SEGMENT_COLORS[i % len(SEGMENT_COLORS)] for i, s in enumerate(segments)}


def _is_share(values: pd.Series) -> bool:
    v = pd.Series(values).dropna()
    return len(v) > 0 and v.min() >= 0 and v.quantile(0.99) <= 1.0 and v.nunique() > 2


def _ship(verdict) -> bool:
    return str(verdict).upper().startswith("SHIP")


def _bar_label(ax, i, x, text, span, size=10.5, bold=True):
    ax.text(x + (0.025 * span if x >= 0 else -0.025 * span), i, text, va="center",
            ha="left" if x >= 0 else "right", fontsize=size, fontweight="bold" if bold else "normal", color=PALETTE["ink"])


def _pivot_effects(effects: pd.DataFrame, value_col: str) -> pd.DataFrame:
    need = {"feature", "segment", value_col}
    missing = need - set(effects.columns)
    if missing:
        raise ValueError(f"effects is missing columns {sorted(missing)}")
    return effects.pivot_table(index="feature", columns="segment", values=value_col, aggfunc="first")


def _labels(effects: pd.DataFrame) -> dict:
    if "label" in effects.columns:
        return effects.drop_duplicates("feature").set_index("feature")["label"].to_dict()
    return {}


def _verdicts(effects: pd.DataFrame) -> dict:
    if "verdict" in effects.columns:
        return effects.drop_duplicates("feature").set_index("feature")["verdict"].to_dict()
    return {}


# ---------------------------------------------------------------------------------------------------------------
# 1. What moves the outcome - one panel per segment (+1 SD or p10 -> p90)
# ---------------------------------------------------------------------------------------------------------------
def effect_bars(effects: pd.DataFrame, segments: Sequence[str], unit: Units, *, value_col: str = "effect",
                seg_labels: dict | None = None, seg_means: dict | None = None, seg_colors: dict | None = None,
                top_n: int = 12, ship_only: bool = True, sort_by: str = "mean_abs",
                title: str = "What moves the outcome", metric_note: str = "change for a +1 SD move from each member's own level",
                note: str = DEFAULT_FOOTNOTE, out_dir: str | None = None, name: str = "effect_bars"):
    """Side-by-side bars, one panel per segment, same lever order in every panel.

    effects   long table, one row per feature x segment:
              feature, segment, effect (or value_col), [label], [verdict]
    sort_by   "mean_abs" (average |effect| across segments) or a segment id (|effect| in that segment)
    """
    apply_style()
    seg_labels = seg_labels or {s: s for s in segments}
    colors = _seg_colors(segments, seg_colors)
    wide = _pivot_effects(effects, value_col).reindex(columns=list(segments))
    lab, ver = _labels(effects), _verdicts(effects)
    if ship_only and ver:
        wide = wide.loc[[f for f in wide.index if _ship(ver.get(f))]]
    order = wide.abs().mean(axis=1) if sort_by == "mean_abs" else wide[sort_by].abs()
    wide = wide.loc[order.sort_values(ascending=False).index[:top_n]].iloc[::-1]
    if wide.empty:
        raise ValueError("no levers to draw (check ship_only / verdict values)")

    fig, axes = plt.subplots(1, len(segments), figsize=(7 * len(segments), 0.52 * len(wide) + 2.2), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, s in zip(axes, segments):
        v = wide[s].fillna(0.0).values
        ax.barh(range(len(v)), v, color=[PALETTE["up"] if x > 0 else PALETTE["down"] for x in v], height=0.62,
                edgecolor="white", linewidth=2)
        span = max(np.abs(v).max(), 1e-9)
        for i, x in enumerate(v):
            _bar_label(ax, i, x, unit.signed(x), span, size=9.5, bold=False)
        ax.axvline(0, color="#8a8984", lw=1)
        ax.set_xlim(-span * 1.35, span * 1.35)
        ax.xaxis.set_major_formatter(unit.axis_formatter(1 if span < 5 else 0))
        t = seg_labels.get(s, s) + (f"  (avg {unit.fmt(seg_means[s])})" if seg_means and s in seg_means else "")
        ax.set_title(t, fontsize=11.5, color=colors[s])
        ax.grid(axis="x", color=PALETTE["grid"], lw=0.8); ax.set_axisbelow(True)
    axes[0].set_yticks(range(len(wide)))
    axes[0].set_yticklabels([lab.get(f, f) for f in wide.index], fontsize=10)
    fig.suptitle(f"{title}: {metric_note}", x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    footnote(fig, "Blue = goes with a higher outcome, red = lower. Every other member attribute held as it is. " + note)
    save_fig(fig, name, out_dir)
    return fig


def effect_bars_single(effects: pd.DataFrame, segment: str, unit: Units, *, value_col: str = "effect",
                       seg_label: str | None = None, seg_mean: float | None = None, top_n: int = 12,
                       ship_only: bool = True, title: str = "What moves the outcome",
                       note: str = DEFAULT_FOOTNOTE, out_dir: str | None = None, name: str = "effect_bars_single"):
    """One-segment, slide-ready version (bold labels, values on the bars). Same input as effect_bars."""
    apply_style()
    wide = _pivot_effects(effects, value_col)
    lab, ver = _labels(effects), _verdicts(effects)
    s = wide[segment].dropna()
    if ship_only and ver:
        s = s[[f for f in s.index if _ship(ver.get(f))]]
    s = s.reindex(s.abs().sort_values(ascending=False).index[:top_n]).iloc[::-1]
    fig, ax = plt.subplots(figsize=(12, 0.52 * len(s) + 1.8))
    v = s.values
    ax.barh(range(len(v)), v, color=[PALETTE["up"] if x > 0 else PALETTE["down"] for x in v], height=0.62,
            edgecolor="white", linewidth=2)
    span = max(np.abs(v).max(), 1e-9)
    for i, x in enumerate(v):
        _bar_label(ax, i, x, unit.signed(x), span, size=12)
    ax.axvline(0, color="#8a8984", lw=1)
    ax.set_xlim(-span * 1.5, span * 1.5)
    ax.set_yticks(range(len(v))); ax.set_yticklabels([lab.get(f, f) for f in s.index], fontsize=11.5, fontweight="bold")
    ax.set_xticks([]); ax.tick_params(left=False); clean_axes(ax)
    t = f"{title} - {seg_label or segment}" + (f"  (avg {unit.fmt(seg_mean, 1)})" if seg_mean is not None else "")
    ax.set_title(t, loc="left", fontsize=13.5, fontweight="bold", pad=12)
    fig.tight_layout()
    footnote(fig, "Blue = goes with a higher outcome, red = lower. " + note, size=9)
    save_fig(fig, name, out_dir)
    return fig


# ---------------------------------------------------------------------------------------------------------------
# 2. Full ranking - recommended and held levers together, held in grey
# ---------------------------------------------------------------------------------------------------------------
def ranking_bars(effects: pd.DataFrame, segment: str, unit: Units, *, value_col: str = "effect", top_n: int = 50,
                 seg_label: str | None = None, title: str = "Every lever, ranked by size",
                 note: str = DEFAULT_FOOTNOTE, out_dir: str | None = None, name: str = "ranking_bars"):
    """All levers for one segment by |effect|; SHIP coloured by direction, everything else grey and tagged (HOLD).

    effects   feature, segment, effect, verdict, [label]
    """
    apply_style()
    wide = _pivot_effects(effects, value_col)
    lab, ver = _labels(effects), _verdicts(effects)
    s = wide[segment].dropna()
    s = s.reindex(s.abs().sort_values(ascending=False).index[:top_n]).iloc[::-1]
    fig, ax = plt.subplots(figsize=(12, 0.45 * len(s) + 2))
    v = s.values
    cols = [(PALETTE["up"] if x > 0 else PALETTE["down"]) if _ship(ver.get(f)) else PALETTE["hold"] for f, x in zip(s.index, v)]
    ax.barh(range(len(v)), v, color=cols, height=0.62, edgecolor="white", linewidth=1.5)
    span = max(np.abs(v).max(), 1e-9)
    for i, x in enumerate(v):
        _bar_label(ax, i, x, unit.signed(x), span, size=9.5)
    ax.axvline(0, color="#8a8984", lw=1); ax.set_xlim(-span * 1.6, span * 1.6)
    ax.set_yticks(range(len(v)))
    ax.set_yticklabels([lab.get(f, f) + ("" if _ship(ver.get(f)) else "  (HOLD)") for f in s.index], fontsize=10)
    ax.set_xticks([]); ax.tick_params(left=False); clean_axes(ax)
    ax.set_title(f"{title} - {seg_label or segment}  (top {len(s)} of {wide[segment].notna().sum()})", loc="left",
                 fontsize=13.5, fontweight="bold", pad=12)
    ax.legend(handles=[Patch(color=PALETTE["up"], label="Recommended - higher outcome"),
                       Patch(color=PALETTE["down"], label="Recommended - lower outcome"),
                       Patch(color=PALETTE["hold"], label="Held - shown for reference only")],
              loc="lower right", frameon=False, fontsize=9.5)
    fig.tight_layout()
    footnote(fig, "Grey bars did not pass every recommendation gate (significance, stability, size, raw-data check, owned "
                  "surface) and are not recommended actions. " + note)
    save_fig(fig, name, out_dir)
    return fig


# ---------------------------------------------------------------------------------------------------------------
# 3. Marginal-effect curves - one behaviour, segments side by side
# ---------------------------------------------------------------------------------------------------------------
def marginal_curve(curves: pd.DataFrame, summary: pd.DataFrame, feature: str, segments: Sequence[str], unit: Units, *,
                   label: str | None = None, explanation: str = "", verdict: str = "", rank: int | None = None,
                   seg_labels: dict | None = None, seg_means: dict | None = None, seg_colors: dict | None = None,
                   min_y_span: dict | float | None = None, binary_labels: tuple = ("No", "Yes"),
                   note: str = DEFAULT_FOOTNOTE, out_dir: str | None = None, name: str | None = None):
    """Predicted outcome as one behaviour moves, every other attribute held as it is (partial dependence).

    curves    segment, feature, x, y            - the curve: predicted outcome at each value of the behaviour
    summary   segment, feature, baseline_x, baseline_y, p10, p90, [per_sd], [p]
              baseline = the segment's average member; p10 / p90 = the segment's spread of the behaviour;
              per_sd / p = the headline effect from your effects table (shown in the box when present)
    min_y_span  narrowest y range allowed (outcome units), per segment {seg: span} or one number, so a small
                effect is never drawn as a cliff. Default: 10% of the segment's baseline.
    """
    apply_style()
    seg_labels = seg_labels or {s: s for s in segments}
    colors = _seg_colors(segments, seg_colors)
    label = label or feature
    fig, axes = plt.subplots(1, len(segments), figsize=(7 * len(segments), 5.4))
    axes = np.atleast_1d(axes)
    for ax, s in zip(axes, segments):
        g = curves[(curves.feature == feature) & (curves.segment == s)].sort_values("x")
        m = summary[(summary.feature == feature) & (summary.segment == s)]
        if g.empty or m.empty:
            ax.axis("off"); continue
        m = m.iloc[0]
        bx, by, q10, q90 = (float(m[k]) for k in ("baseline_x", "baseline_y", "p10", "p90"))
        binary = g.x.nunique() <= 2
        y10, y90 = np.interp([q10, q90], g.x, g.y)
        d = float(y90 - y10)
        c = colors[s]
        if not binary:
            ax.axvspan(q10, q90, color=c, alpha=0.07, lw=0)
        ax.plot(g.x, g.y, color=c, linewidth=2.5, marker="o", ms=6)
        ax.axhline(by, color="#8a8984", ls="--", lw=1.1)
        ax.axvline(bx, color=PALETTE["ink_2"], ls=":", lw=1.1)
        ax.scatter([bx], [by], color=PALETTE["ink"], s=45, zorder=3)
        ax.annotate(f"Average member\n{unit.fmt(by, 1)}", xy=(bx, by), xytext=(8, 8), textcoords="offset points", fontsize=9.5)
        box = f"{'0 → 1' if binary else 'Low (p10) → high (p90)'}:  {unit.fmt(y10, 1)} → {unit.fmt(y90, 1)} ({unit.signed(d)})"
        if "per_sd" in m and pd.notna(m.get("per_sd")):
            box += f"\nPer +1 SD: {unit.signed(float(m['per_sd']))}" + (f"   p={float(m['p']):.2g}" if pd.notna(m.get("p", np.nan)) else "")
        ax.text(0.98, 0.04 if d >= 0 else 0.96, box, transform=ax.transAxes, ha="right", va="bottom" if d >= 0 else "top",
                fontsize=9.5, fontweight="bold", color=PALETTE["up"] if d >= 0 else PALETTE["down"],
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#d9d8d3"))
        span_min = (min_y_span.get(s) if isinstance(min_y_span, dict) else min_y_span) or 0.10 * abs(by)
        lo, hi = float(g.y.min()), float(g.y.max())
        span = max((hi - lo) * 1.6, span_min); mid = (hi + lo) / 2
        ax.set_ylim(mid - span / 2, mid + span / 2)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _, dp=(1 if span < 40 else 0): unit.fmt(v, dp)))
        if _is_share(g.x):
            ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        if binary:
            xs = sorted(g.x.unique()); ax.set_xticks(xs)
            ax.set_xticklabels(list(binary_labels) if xs == [0.0, 1.0] else [f"{x:g}" for x in xs])
        t = seg_labels.get(s, s) + (f"  (avg {unit.fmt(seg_means[s], 1)})" if seg_means and s in seg_means else "")
        ax.set_title(t, fontsize=11.5, color=c)
        ax.set_xlabel(label); ax.set_ylabel(f"Predicted outcome ({unit.symbol}{' ' + unit.per if unit.per else ''})")
        ax.grid(alpha=0.25)
    head = (f"#{rank}  " if rank else "") + label + (f"   [{verdict}]" if verdict else "")
    fig.suptitle(head, x=0.01, ha="left", fontsize=14, fontweight="bold")
    if explanation:
        fig.text(0.01, 0.925, textwrap.fill(explanation, 150), ha="left", va="top", fontsize=10, color=PALETTE["ink_2"])
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    footnote(fig, "Shaded band = the segment's p10 to p90 of the behaviour. One model, averaged over each segment's own "
                  "members; every other attribute kept as it is. " + note)
    save_fig(fig, name or f"marginal_{rank or ''}_{feature}", out_dir)
    return fig


def marginal_curves(curves: pd.DataFrame, summary: pd.DataFrame, features: Iterable[str], segments: Sequence[str],
                    unit: Units, *, labels: dict | None = None, explanations: dict | None = None,
                    verdicts: dict | None = None, show: bool = True, **kw):
    """marginal_curve for each feature in order (rank = position). Returns the list of figures."""
    figs = []
    for r, f in enumerate(features, 1):
        fig = marginal_curve(curves, summary, f, segments, unit, label=(labels or {}).get(f, f),
                             explanation=(explanations or {}).get(f, ""), verdict=(verdicts or {}).get(f, ""), rank=r,
                             name=f"marginal_{r:02d}_{f}", **kw)
        figs.append(fig)
        if show:
            plt.show()
    return figs


# ---------------------------------------------------------------------------------------------------------------
# 4. What predicts the outcome - all features, context vs lever
# ---------------------------------------------------------------------------------------------------------------
def importance_bars(importance: pd.DataFrame, *, top_n: int = 20, outcome: str = "the outcome",
                    note: str = "", out_dir: str | None = None, name: str = "importance_all_features"):
    """Permutation importance for every model input, coloured by role.

    importance  feature, share (% of total importance, 0-100), role ("Lever" | "Context" | "Coverage flag"),
                [label], [verdict] (SHIP / HOLD for levers), [raw_direction] (short text, e.g. "more of it goes with
                bigger baskets")
    """
    apply_style()
    d = importance.sort_values("share", ascending=False).head(top_n).iloc[::-1]
    role_col = {"Lever": PALETTE["up"], "Context": PALETTE["context"], "Coverage flag": PALETTE["flag"]}
    tot = importance.groupby("role")["share"].sum()
    fig, ax = plt.subplots(figsize=(12.5, 0.48 * len(d) + 2.2))
    v = d.share.values
    ax.barh(range(len(d)), v, color=[role_col.get(r, PALETTE["hold"]) for r in d.role], height=0.64, edgecolor="white", linewidth=1.5)
    for i, (_, r) in enumerate(d.iterrows()):
        extra = f"   ({r['raw_direction']})" if "raw_direction" in d and isinstance(r.get("raw_direction"), str) and r["raw_direction"] else ""
        ax.text(r.share + 0.012 * max(v.max(), 1), i, f"{r.share:.1f}%{extra}", va="center", fontsize=9.5)

    def _tag(r):
        lab = r.get("label", r["feature"]) if isinstance(r.get("label", None), str) else r["feature"]
        if r.role == "Lever" and isinstance(r.get("verdict", None), str):
            return lab + ("  · SHIP" if _ship(r["verdict"]) else "  · HOLD")
        return lab + ("  · context" if r.role == "Context" else "")
    ax.set_yticks(range(len(d))); ax.set_yticklabels([_tag(r) for _, r in d.iterrows()], fontsize=10.5)
    ax.set_xlim(0, v.max() * 1.9 if len(v) else 1); ax.set_xticks([]); ax.tick_params(left=False); clean_axes(ax)
    ax.set_title(f"What predicts {outcome} - all features (top {len(d)} of {len(importance)})", loc="left",
                 fontsize=13.5, fontweight="bold", pad=12)
    ax.legend(handles=[Patch(color=PALETTE["context"], label=f"Context - who to target ({tot.get('Context', 0):.0f}% of importance)"),
                       Patch(color=PALETTE["up"], label=f"Lever - what the business can move ({tot.get('Lever', 0):.0f}%)"),
                       Patch(color=PALETTE["flag"], label=f"Coverage flag ({tot.get('Coverage flag', 0):.0f}%)")],
              loc="lower right", frameon=False, fontsize=9.5)
    fig.tight_layout()
    footnote(fig, "Share of total permutation importance on held-out rows. Features that move together share importance, "
                  "so read ranks and the context / lever split, not exact shares. Context is for targeting; only levers "
                  "are candidate actions. " + note)
    save_fig(fig, name, out_dir)
    return fig


# ---------------------------------------------------------------------------------------------------------------
# 5. Model fit - context only vs context + behaviours, within each segment
# ---------------------------------------------------------------------------------------------------------------
def fit_bars(fit: pd.DataFrame, *, outcome: str = "the outcome", seg_labels: dict | None = None,
             context_label: str = "Context only: who the member is", all_label: str = "Context + behaviours (levers)",
             note: str = "", out_dir: str | None = None, name: str = "model_fit"):
    """Held-out R2 inside each segment, two bars per segment, with the gain the behaviours add.

    fit   segment, r2_context, r2_all   (R2 on 0-1 scale, measured within the segment)
    """
    apply_style()
    seg_labels = seg_labels or {}
    fig, ax = plt.subplots(figsize=(12, 4.8))
    xs, w = np.arange(len(fit)), 0.36
    ax.bar(xs - w / 2, fit.r2_context, w, color=PALETTE["hold"], edgecolor="white", linewidth=2, label=context_label)
    ax.bar(xs + w / 2, fit.r2_all, w, color=PALETTE["up"], edgecolor="white", linewidth=2, label=all_label)
    top = max(fit.r2_all.max(), fit.r2_context.max())
    for x, a, b in zip(xs, fit.r2_context, fit.r2_all):
        ax.text(x - w / 2, a + 0.01, f"{a:.0%}", ha="center", va="bottom", fontsize=12, fontweight="bold")
        ax.text(x + w / 2, b + 0.01, f"{b:.0%}", ha="center", va="bottom", fontsize=12, fontweight="bold")
        ax.annotate(f"behaviours add {100 * (b - a):+.0f} pts", xy=(x, max(a, b) + 0.07), ha="center", fontsize=10.5,
                    color=PALETTE["up"], fontweight="bold")
    ax.set_xticks(xs); ax.set_xticklabels([seg_labels.get(s, s) for s in fit.segment], fontsize=11)
    ax.set_ylim(0, min(1.05, top + 0.28)); ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    ax.set_ylabel(f"Share of variation in {outcome} explained\n(held-out members, within segment)")
    ax.grid(axis="y", color=PALETTE["grid"]); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    ax.set_title(f"How much of the difference in {outcome} can we explain?", loc="left", fontsize=13)
    fig.tight_layout()
    footnote(fig, "R2 on held-out members inside each segment. Each segment is a narrow band of the outcome, so "
                  "within-segment R2 is low by construction; a pooled R2 across segments cut on the outcome itself "
                  "would overstate the model. " + note, y=-0.04)
    save_fig(fig, name, out_dir)
    return fig


# ---------------------------------------------------------------------------------------------------------------
# 6. Gap decomposition - where the difference between two groups sits, by category (arithmetic, no model)
# ---------------------------------------------------------------------------------------------------------------
def gap_bars(gap: pd.DataFrame, unit: Units, *, low_name: str = "Low group", high_name: str = "High group",
             title: str | None = None, min_abs: float = 0.005, note: str = "", out_dir: str | None = None,
             name: str = "gap_by_category"):
    """Bars of (high - low) per category, labelled with $ and share of the total gap.

    gap   category, low_value, high_value   - per-category pieces that ADD UP to each group's total (e.g. $ per order
          by GMM summing to AOV), so the bars add up to the whole gap
    """
    apply_style()
    d = gap.assign(gap=gap.high_value - gap.low_value)
    total = float(d.gap.sum())
    d["share"] = 100 * d.gap / total if abs(total) > 1e-12 else np.nan
    d = d[d.gap.abs() > min_abs].sort_values("gap", ascending=False).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 0.55 * max(len(d), 3) + 1.8))
    ax.barh(range(len(d)), d.gap, color=[PALETTE["up"] if x > 0 else PALETTE["down"] for x in d.gap], height=0.62,
            edgecolor="white", linewidth=2)
    span = max(d.gap.abs().max(), 1e-9)
    for i, (x, sh) in enumerate(zip(d.gap, d.share)):
        _bar_label(ax, i, x, f"{unit.signed(x)}  ({sh:.0f}% of gap)", span, size=10, bold=False)
    ax.axvline(0, color="#8a8984", lw=1)
    ax.set_xlim(-span * 0.15 if d.gap.min() >= 0 else -span * 1.6, span * 1.6)
    ax.set_yticks(range(len(d))); ax.set_yticklabels(d.category, fontsize=11)
    ax.xaxis.set_major_formatter(unit.axis_formatter())
    ax.grid(axis="x", color=PALETTE["grid"]); ax.set_axisbelow(True)
    ax.set_title(title or f"{high_name} - {low_name}, split by category: {unit.signed(total)}", loc="left", fontsize=13)
    fig.tight_layout()
    footnote(fig, "Arithmetic, not a model: each category's piece adds back to the group total, so the bars add up to "
                  "the whole gap. It shows where the difference sits, not what causes it. " + note)
    save_fig(fig, name, out_dir)
    return fig


# ---------------------------------------------------------------------------------------------------------------
# 7. Scorecard - the behaviour -> effect -> verdict -> action table
# ---------------------------------------------------------------------------------------------------------------
SCORECARD_COLS = ["behaviour", "feature", "effect_seg_1", "effect_seg_2", "p", "verdict", "action"]


def scorecard_table(scorecard: pd.DataFrame, unit: Units, *, seg_names: tuple = ("Segment 1", "Segment 2")):
    """Notebook view (pandas Styler): SHIP rows bold, held rows grey, effects signed and coloured.

    scorecard  behaviour, feature, effect_seg_1, effect_seg_2, p, verdict, action   (extra columns are kept)
    """
    d = scorecard.rename(columns={"effect_seg_1": f"effect {seg_names[0]}", "effect_seg_2": f"effect {seg_names[1]}"})
    eff_cols = [f"effect {seg_names[0]}", f"effect {seg_names[1]}"]

    def _row(r):
        ship = _ship(r.get("verdict", ""))
        return [("font-weight:600;" if ship else f"color:{PALETTE['ink_2']};") for _ in r]

    def _eff(v):
        if pd.isna(v):
            return ""
        return f"color:{PALETTE['up'] if v > 0 else PALETTE['down']};"
    sty = d.style.apply(_row, axis=1)
    sty = sty.map(_eff, subset=eff_cols) if hasattr(sty, "map") else sty.applymap(_eff, subset=eff_cols)
    return (sty
             .format({c: (lambda v: unit.signed(v)) for c in eff_cols} | ({"p": "{:.3g}"} if "p" in d else {}))
             .hide(axis="index"))


def scorecard_figure(scorecard: pd.DataFrame, unit: Units, *, seg_names: tuple = ("Segment 1", "Segment 2"),
                     title: str = "Behaviour scorecard", max_rows: int = 14, wrap: int = 52,
                     out_dir: str | None = None, name: str = "scorecard"):
    """Slide-ready image of the scorecard (top max_rows rows, SHIP first). Same input as scorecard_table."""
    apply_style()
    d = scorecard.copy()
    d["is_ship"] = d.verdict.map(_ship)
    d = d.sort_values(["is_ship"], ascending=False).head(max_rows)
    head = ["Behaviour", seg_names[0], seg_names[1], "Verdict", "Action"]
    cells = [[textwrap.fill(str(r.behaviour), 30), unit.signed(r.effect_seg_1), unit.signed(r.effect_seg_2),
              "SHIP" if r.is_ship else textwrap.fill(str(r.verdict).replace("HOLD - ", "HOLD: "), 28),
              textwrap.fill(str(r.action or ""), wrap)] for r in d.itertuples()]
    fig, ax = plt.subplots(figsize=(15, 0.62 * len(cells) + 1.4)); ax.axis("off")
    tb = ax.table(cellText=cells, colLabels=head, loc="upper left", cellLoc="left", colLoc="left",
                  colWidths=[0.2, 0.09, 0.09, 0.18, 0.44])
    tb.auto_set_font_size(False); tb.set_fontsize(9.5); tb.scale(1, 2.4)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor(PALETTE["grid"])
        if r == 0:
            cell.set_facecolor(PALETTE["up"]); cell.get_text().set_color("white"); cell.get_text().set_weight("bold")
        else:
            row = d.iloc[r - 1]
            if not row.is_ship:
                cell.get_text().set_color(PALETTE["ink_2"]); cell.set_facecolor("#f7f5ef")
            if c in (1, 2):
                v = row.effect_seg_1 if c == 1 else row.effect_seg_2
                cell.get_text().set_color(PALETTE["up"] if v > 0 else PALETTE["down"]); cell.get_text().set_weight("bold")
    ax.set_title(title, loc="left", fontsize=13.5, fontweight="bold")
    save_fig(fig, name, out_dir)
    return fig


# ---------------------------------------------------------------------------------------------------------------
# 8. Where the two segments sit - distributions of the top behaviours
# ---------------------------------------------------------------------------------------------------------------
def segment_distributions(frame: pd.DataFrame, features: Sequence[str], segments: Sequence[str], *,
                          segment_col: str = "segment", labels: dict | None = None, seg_labels: dict | None = None,
                          seg_colors: dict | None = None, ncols: int = 3, bins: int = 40,
                          title: str = "Where the segments sit on the behaviours that matter (dotted = median)",
                          out_dir: str | None = None, name: str = "segment_distributions"):
    """Step histograms per segment, one small panel per behaviour (member-level frame: segment + feature columns)."""
    apply_style()
    labels, seg_labels = labels or {}, seg_labels or {}
    colors = _seg_colors(segments, seg_colors)
    feats = [f for f in features if f in frame.columns]
    nr = int(np.ceil(len(feats) / ncols))
    fig, axes = plt.subplots(nr, ncols, figsize=(14, 3.4 * nr)); axes = np.atleast_1d(axes).flatten()
    for ax in axes[len(feats):]:
        ax.axis("off")
    for ax, f in zip(axes, feats):
        lo, hi = frame[f].quantile([0.01, 0.99]); edges = np.linspace(lo, hi, bins)
        for s in segments:
            v = frame.loc[frame[segment_col] == s, f].clip(lo, hi)
            ax.hist(v, bins=edges, density=True, histtype="step", lw=2, color=colors[s], label=seg_labels.get(s, s))
            ax.axvline(v.median(), color=colors[s], ls=":", lw=1.4)
        ax.set_title(textwrap.fill(labels.get(f, f), 38), fontsize=10.5); ax.set_yticks([])
        if _is_share(frame[f]):
            ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
        ax.spines["left"].set_visible(False); ax.grid(axis="x", color=PALETTE["grid"])
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper right")
    fig.suptitle(title, x=0.01, ha="left", fontsize=12.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save_fig(fig, name, out_dir)
    return fig

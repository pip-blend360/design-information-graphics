"""Optional: turn the objects of a ship / hold driver-model notebook into the tables ds_charts expects.

Written for the two-segment XGBoost pipeline these charts came from (bootstrapped average marginal effects,
partial-dependence curves, permutation importance, SHIP / HOLD gates). If your notebook names things differently,
copy one function and change the column names - the target table shapes are what matter.

    effects   = effects_from_ship(ship, ame_tab=ame_tab, swing_tab=swing_tab, label=label)
    curves, summary = curves_from_marginal(aov_marginal_pdf, df, LEVER_COLS, coef=coef)
    importance = importance_from_imp_all(IMP_ALL, ship=ship, label=label)
    fit       = fit_from_r2tab(r2tab, segments=SEGS)
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def effects_from_ship(ship: pd.DataFrame, *, ame_tab: pd.DataFrame | None = None, swing_tab: pd.DataFrame | None = None,
                      segments: list | None = None, model: str = "XGBoost", label=None) -> pd.DataFrame:
    """ship: index = feature, columns incl. 'per SD <KEY>' and 'verdict' (KEY = first token of each segment id).
    ame_tab / swing_tab: index = feature, columns MultiIndex (segment, model) - per +1 SD and p10->p90 effects."""
    rows = []
    segs = segments or ([s for s in ame_tab.columns.get_level_values(0).unique()] if ame_tab is not None else [])
    for f in ship.index:
        for s in segs:
            k = s.split("_")[0]
            e = (float(ame_tab.loc[f, (s, model)]) if ame_tab is not None and f in ame_tab.index
                 else float(ship.loc[f, f"per SD {k}"]))
            sw = float(swing_tab.loc[f, (s, model)]) if swing_tab is not None and f in swing_tab.index else np.nan
            rows.append({"feature": f, "label": label(f) if label else f, "segment": s, "effect": e, "p10_p90": sw,
                         "verdict": ship.loc[f, "verdict"], "p": float(ship.loc[f, f"p {k}"]) if f"p {k}" in ship else np.nan})
    return pd.DataFrame(rows)


def curves_from_marginal(marginal_pdf: pd.DataFrame, frame: pd.DataFrame, features, *, coef: pd.DataFrame | None = None,
                         model: str = "XGBoost", y_col: str = "predicted_aov") -> tuple[pd.DataFrame, pd.DataFrame]:
    """marginal_pdf: segment, model, feature_name, feature_value, <y_col>, baseline_feature_value, baseline_predicted_aov.
    frame: member-level, with 'segment' and the raw feature columns (for p10 / p90)."""
    m = marginal_pdf[(marginal_pdf.model == model) & (marginal_pdf.feature_name.isin(list(features)))]
    curves = m.rename(columns={"feature_name": "feature", "feature_value": "x", y_col: "y"})[["segment", "feature", "x", "y"]]
    rows = []
    for (s, f), g in m.groupby(["segment", "feature_name"]):
        x = frame.loc[frame.segment == s, f].dropna()
        k = s.split("_")[0]
        rows.append({"segment": s, "feature": f, "baseline_x": float(g.baseline_feature_value.iloc[0]),
                     "baseline_y": float(g.baseline_predicted_aov.iloc[0]),
                     "p10": float(x.min() if x.nunique() <= 2 else x.quantile(0.10)),
                     "p90": float(x.max() if x.nunique() <= 2 else x.quantile(0.90)),
                     "per_sd": float(coef.loc[f, f"per SD {k}"]) if coef is not None and f in coef.index else np.nan,
                     "p": float(coef.loc[f, f"p {k}"]) if coef is not None and f in coef.index else np.nan})
    return curves.reset_index(drop=True), pd.DataFrame(rows)


def importance_from_imp_all(imp_all: pd.DataFrame, *, ship: pd.DataFrame | None = None, label=None,
                            raw_direction=None) -> pd.DataFrame:
    """imp_all: index = feature, columns 'share %' and 'role'."""
    d = imp_all.reset_index().rename(columns={"index": "feature", "share %": "share"})
    if "feature" not in d.columns:
        d = d.rename(columns={d.columns[0]: "feature"})
    d["label"] = [label(f) if label else f for f in d.feature]
    if ship is not None:
        d["verdict"] = [ship.loc[f, "verdict"] if f in ship.index else None for f in d.feature]
    if raw_direction is not None:
        d["raw_direction"] = [raw_direction(f) for f in d.feature]
    return d[[c for c in ["feature", "label", "share", "role", "verdict", "raw_direction"] if c in d.columns]]


def fit_from_r2tab(r2tab: pd.DataFrame, segments: list) -> pd.DataFrame:
    """r2tab: index = fit name (one row per segment), columns 'R2 controls', 'R2 + levers'."""
    return pd.DataFrame({"segment": segments,
                         "r2_context": [float(r2tab.loc[s, "R2 controls"]) for s in segments],
                         "r2_all": [float(r2tab.loc[s, "R2 + levers"]) for s in segments]})

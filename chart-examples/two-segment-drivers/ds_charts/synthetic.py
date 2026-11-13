"""Synthetic demo data in exactly the shape every ds_charts function expects.

Nothing here is real: invented behaviours, invented effects, two generic segments. Use it to try the charts,
to test a change to the library, or as the reference for the input columns.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SEGMENTS = ["SEG_MID", "SEG_HIGH"]
SEG_LABELS = {"SEG_MID": "Mid segment", "SEG_HIGH": "High segment"}

# feature, label, kind ("share" | "count" | "binary"), true effect per SD (mid, high), verdict, action
_LEVERS = [
    ("pickup_share", "Pickup share of orders", "share", (1.8, 3.9), "SHIP", "Pickup basket builder and a spend threshold on pickup orders"),
    ("pages_per_visit", "Pages per visit", "count", (2.6, 5.1), "SHIP", "Curated collections and recommendations"),
    ("channels_used", "Fulfilment channels used", "count", (1.5, 3.2), "SHIP", "Introduce a second fulfilment option"),
    ("grocery_share_ly", "Grocery share of spend (last year)", "share", (1.2, 2.7), "SHIP", "Bulk-pack and multi-buy grocery offers"),
    ("event_families", "Event families shopped", "count", (0.9, 2.2), "SHIP", "Cross-event bundles"),
    ("app_order_share", "Orders placed on the app", "share", (-1.4, -2.6), "SHIP", "App basket builder before checkout"),
    ("discount_floor", "Shallowest discount that converts them", "share", (-4.8, -9.5), "SHIP", "Spend-threshold offers instead of deeper discounts"),
    ("conversion_rate", "Visit-to-order conversion", "share", (-2.1, -4.4), "SHIP", "Basket threshold on quick top-up orders"),
    ("dmm_per_order_ly", "DMMs per order (last year)", "count", (-1.1, -2.3), "HOLD - opposite sign to the raw data", "Cross-department prompts"),
    ("promo_lift", "Rest-of-basket lift on promo orders", "share", (-3.3, -6.1), "HOLD - opposite sign to the raw data", "Pair the deal with a complementary item"),
    ("push_optin", "Opted in to push notifications", "binary", (-0.2, -0.3), "HOLD - not significant", "Opt-in prompts, then basket-building pushes"),
    ("reorder_adds", "Visits adding from Reorder", "share", (0.6, 1.1), "SHIP", "Multi-item buy-it-again"),
]
_CONTEXT = [("aov_last_year", "Basket size last year"), ("orders_this_year", "Orders this year"),
            ("inclub_basket", "In-club basket size"), ("tenure_yrs", "Membership tenure (years)"), ("age", "Age")]


def make_example_tables(seed: int = 7, n_members: int = 4000) -> dict:
    """Return every input table the charts take: effects, curves, summary, importance, fit, gap, scorecard, frame."""
    rng = np.random.default_rng(seed)
    means = {"SEG_MID": 60.0, "SEG_HIGH": 110.0}

    # ---- member-level frame (for distributions) and per-segment quantiles ----
    rows = []
    for s in SEGMENTS:
        n = n_members // 2
        lift = 0.0 if s == "SEG_MID" else 1.0
        rec = {"segment": [s] * n}
        for f, _, kind, *_ in _LEVERS:
            if kind == "share":
                rec[f] = np.clip(rng.beta(2 + lift, 4, n), 0, 1)
            elif kind == "count":
                rec[f] = np.round(rng.gamma(3 + lift, 1.0, n), 1)
            else:
                rec[f] = (rng.random(n) < 0.6 + 0.1 * lift).astype(float)
        rows.append(pd.DataFrame(rec))
    frame = pd.concat(rows, ignore_index=True)

    # ---- effects (long), curves, summary ----
    eff, curves, summ = [], [], []
    for f, lab, kind, (em, eh), verdict, action in _LEVERS:
        for s, e in zip(SEGMENTS, (em, eh)):
            x = frame.loc[frame.segment == s, f]
            sd = float(x.std()) or 1.0
            q10, q90 = (float(v) for v in x.quantile([0.10, 0.90]))
            base_x = float(x.mean())
            grid = np.unique([0.0, 1.0]) if kind == "binary" else np.unique(x.quantile([0.05, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 0.95]).values)
            bend = 1 + 0.25 * np.tanh((grid - base_x) / sd)                       # mild curvature, monotone
            y = means[s] + e * (grid - base_x) / sd * bend + rng.normal(0, abs(e) * 0.03, len(grid))
            base_y = float(np.interp(base_x, grid, y)) if len(grid) > 1 else means[s]
            swing = float(np.interp(q90, grid, y) - np.interp(q10, grid, y))
            eff.append({"feature": f, "label": lab, "segment": s, "effect": e, "p10_p90": swing, "verdict": verdict,
                        "p": 1e-6 if verdict == "SHIP" else 0.2})
            curves += [{"segment": s, "feature": f, "x": float(gx), "y": float(gy)} for gx, gy in zip(grid, y)]
            summ.append({"segment": s, "feature": f, "baseline_x": base_x, "baseline_y": base_y, "p10": q10, "p90": q90,
                         "per_sd": e, "p": 1e-6 if verdict == "SHIP" else 0.2})
    effects, curves, summary = pd.DataFrame(eff), pd.DataFrame(curves), pd.DataFrame(summ)

    # ---- importance (all features, three roles) ----
    imp = [{"feature": f, "label": lab, "role": "Context", "share": sh, "raw_direction": "more of it goes with a bigger outcome"}
           for (f, lab), sh in zip(_CONTEXT, [18.0, 4.5, 3.0, 2.0, 0.8])]
    imp += [{"feature": f, "label": lab, "role": "Lever", "share": sh, "verdict": v,
             "raw_direction": "more of it goes with a bigger outcome" if (em + eh) > 0 else "more of it goes with a smaller outcome"}
            for (f, lab, _, (em, eh), v, _a), sh in zip(_LEVERS, [3.1, 2.2, 0.9, 1.6, 0.7, 0.8, 4.4, 1.9, 1.0, 5.5, 0.3, 0.4])]
    imp.append({"feature": "has_visits", "label": "Has any digital visits", "role": "Coverage flag", "share": 0.1})
    importance = pd.DataFrame(imp)
    importance["share"] = 100 * importance.share / importance.share.sum()

    fit = pd.DataFrame({"segment": SEGMENTS, "r2_context": [0.15, 0.22], "r2_all": [0.24, 0.33]})
    gap = pd.DataFrame({"category": ["Grocery", "General Merchandise", "Fresh", "Household", "Services"],
                        "low_value": [22.0, 12.0, 8.0, 16.0, 2.0], "high_value": [40.0, 25.0, 15.0, 24.0, 6.0]})
    sc = effects.pivot_table(index=["feature", "label", "verdict"], columns="segment", values="effect").reset_index()
    scorecard = pd.DataFrame({"behaviour": sc.label, "feature": sc.feature, "effect_seg_1": sc["SEG_MID"],
                              "effect_seg_2": sc["SEG_HIGH"], "p": [1e-6 if v == "SHIP" else 0.2 for v in sc.verdict],
                              "verdict": sc.verdict,
                              "action": [dict((l[0], l[5]) for l in _LEVERS)[f] for f in sc.feature]})
    return dict(effects=effects, curves=curves, summary=summary, importance=importance, fit=fit, gap=gap,
                scorecard=scorecard, frame=frame, segments=SEGMENTS, seg_labels=SEG_LABELS, seg_means=means)

# ds_charts — two-segment driver chart examples

A small matplotlib library for models that compare two segments (e.g. Mid vs High basket size, or Mid vs High
frequency). It answers four questions: *which behaviours go with a better outcome*, *how much*, *how sure are we*,
and *what do we do about it*.

Every function takes a **plain pandas DataFrame** and returns a matplotlib Figure. The functions read no notebook globals. Reuse them when the input contracts and analytical assumptions below fit your comparison.

```
ds_charts/
  style.py       palette, Units (how values are written), save helper
  charts.py      one function per chart
  synthetic.py   demo tables in exactly the expected shape (no real data)
  adapters.py    optional: build the tables from a ship / hold XGBoost driver notebook
example.ipynb    every chart, drawn from synthetic data (already executed)
example_charts/  the PNGs example.ipynb writes
```

**Requirements:** Python ≥ 3.9, pandas ≥ 1.5 (≥ 2.1 for the styled scorecard table), numpy, and matplotlib ≥ 3.6. The styled notebook scorecard also requires Jinja2.

## Quick start

```python
import sys; sys.path.insert(0, "/path/to/folder/containing/ds_charts")
import ds_charts as dc
from ds_charts.synthetic import make_example_tables

T = make_example_tables()                      # replace with your own tables of the same shape
U = dc.Units("$", "per order")                 # or dc.Units("orders", "per year")
dc.effect_bars(T["effects"], T["segments"], U, seg_labels=T["seg_labels"], out_dir="charts")
```

## The charts and the table each one takes

| # | Function | What it shows | Input table (required columns; `[optional]`) |
|---|---|---|---|
| 1 | `effect_bars` | What moves the outcome, one panel per segment, same lever order. Use `value_col="effect"` for the +1 SD effect and `value_col="p10_p90"` for the low → high swing | **effects**: `feature, segment, effect` `[label, verdict, p10_p90]`, one row per feature × segment |
| 1c | `effect_bars_single` | The same for one segment, slide-ready (bold labels, values on the bars) | **effects** |
| 2 | `ranking_bars` | Every lever by size. Recommended levers are coloured by direction; held levers are grey and tagged (HOLD) | **effects** with `verdict` |
| 3 | `marginal_curve` / `marginal_curves` | Predicted outcome as one behaviour moves, segments side by side. Each chart shows the p10–p90 band, the average member, and a box with p10 → p90 and per +1 SD | **curves**: `segment, feature, x, y`. **summary**: `segment, feature, baseline_x, baseline_y, p10, p90` `[per_sd, p]` |
| 4 | `importance_bars` | Everything the model uses, coloured context / lever / flag, with each feature's raw direction | **importance**: `feature, share, role` `[label, verdict, raw_direction]`. `share` is % of total (0–100); `role` ∈ {Lever, Context, Coverage flag} |
| 5 | `fit_bars` | Within-segment R²: context only vs context + behaviours | **fit**: `segment, r2_context, r2_all` (0–1) |
| 6 | `gap_bars` | Where the gap between two groups sits, by category. This is arithmetic, not a model | **gap**: `category, low_value, high_value`. The pieces must add up to each group's total |
| 7 | `scorecard_table` / `scorecard_figure` | Behaviour → effect → verdict → action, as a notebook table or a slide image | **scorecard**: `behaviour, effect_seg_1, effect_seg_2, verdict, action` `[feature, p]` |
| 8 | `segment_distributions` | Where each segment sits on the top behaviours | **frame**: member-level, with `segment` plus one column per feature |

Common arguments:
- `unit`
- `segments` (display order)
- `seg_labels` (id → readable name)
- `seg_means` (shown in panel titles)
- `out_dir` (save PNGs; `None` means don't save)
- `note` (appended to the footnote)

`verdict` values beginning with `SHIP` are recommended. Anything else is treated as held.

## Before reusing a chart

- Validate input against the skill’s data contract. For effect bars, check that feature–segment pairs are unique and that every displayed effect is present and finite. The paired renderer can silently resolve duplicates or display a missing effect as zero.
- For client effect bars, supply a reviewed table of explicitly approved SHIP levers. Check that verdicts agree across segments. The functions can include all levers when verdicts are absent. Use the ranking example when held levers belong in the comparison.
- Review the figure at its intended size. Check shared scales for comparisons, signed values and color cues, and the contrast of any brand palette. Scope the render with Matplotlib’s `rc_context` to contain changes to plotting defaults and check the figure against the selected brand.
- Write notes that match the evidence. Replace the default claim about confirmed lift where a causal test has yet to establish it. For the fit chart, title it to describe within-segment R².
- Apply the skill’s normal review and evidence export. The package’s PNG save helper only saves the figure.

Run `example.ipynb` from this folder to regenerate the synthetic gallery. Inspect the rendered output and check the notebook scorecard as well as the PNGs.

## From an existing ship / hold notebook

Upstream of the skill, `ds_charts.adapters` builds the tables from the objects of the XGBoost driver pipeline the charts came from:
- `ship`, the SHIP / HOLD table;
- `ame_tab` / `swing_tab`, the +1 SD and p10 → p90 effects;
- the partial-dependence frame and `coef`;
- `IMP_ALL`, the permutation importance;
- `r2tab`, the within-segment R².

```python
from ds_charts.adapters import effects_from_ship, curves_from_marginal, importance_from_imp_all, fit_from_r2tab
effects = effects_from_ship(ship, ame_tab=ame_tab, swing_tab=swing_tab, segments=SEGS, label=label)
curves, summary = curves_from_marginal(marginal_pdf, df, LEVER_COLS, coef=coef)
```

If your notebook names things differently, copy one adapter and rename the columns. The target table shapes are
what matter.

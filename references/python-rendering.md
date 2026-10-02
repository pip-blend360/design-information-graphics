# Python Rendering

Target Python 3.11 or later with pandas, Matplotlib, and Seaborn. Use an existing pandas DataFrame in memory. Do not load files or access databases for the user.

Generate reusable functions that accept a DataFrame and return a Matplotlib `Figure`:

```python
def create_program_effect_graphic(data: pd.DataFrame) -> Figure:
    validate_dataframe(data, contract)
    plot_data = data.copy(deep=False)
    fig = plt.figure(figsize=(12, 6.75), constrained_layout=True)
    # Presentation-only ordering and rendering.
    return fig
```

Avoid global state and `inplace=True`. Keep saving outside the construction function. Do not call `plt.show()` inside reusable functions unless requested. Assign the returned figure to a descriptive variable in notebooks. Use Matplotlib for composition and Seaborn only for suitable statistical marks.

Show drafts in the existing notebook. On explicit finalization, save PNG and exact data CSV; SVG is optional when requested or needed by the medium. Leave runnable graph code in the existing notebook or Python package, rather than requiring a standalone code file. Use the graphic ID and matching version suffix as the filename stem, never overwrite silently, and use explicit figure size and DPI. Verify mark counts, ranges, units, labels, annotations, and evidence values; inspect rendered output for clipping, overlap, poor hierarchy, and unintended emphasis.

Disable default statistical aggregation, fitting, binning, and confidence intervals in plotting libraries when rendering prepared values. Load style defaults from `resources/information-graphic.mplstyle` and palette defaults from `resources/default-palette.json` when useful. See `special-cases.md` for available alternative Python renderers and input constraints.

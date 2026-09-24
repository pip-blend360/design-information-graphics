# Python Rendering

Target Python 3.11 or later with pandas, Matplotlib, Seaborn, and PyYAML. Use an existing pandas DataFrame in memory. Do not load files or access databases for the user.

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

Default to PNG and SVG plus Excel-ready CSV evidence and YAML metadata. Use one CSV when every visible panel uses the same grain; use separate, clearly named CSVs when panels use different analysis-ready DataFrames or grains. The CSV files contain data only, not reconstruction or styling instructions. Use the graphic ID as the filename stem, never overwrite silently, and use explicit figure size and DPI. Verify mark counts, ranges, units, labels, annotations, and evidence values; inspect rendered output for clipping, overlap, poor hierarchy, and unintended emphasis.

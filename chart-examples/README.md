# Contributed chart examples

Use this index to find an optional chart example that fits the request. Read the package README for its inputs, assumptions, and review notes before reuse.

| Package | When to look |
| --- | --- |
| [Two-segment driver charts](two-segment-drivers/README.md) | Comparing effects, lever rankings, marginal curves, feature importance, within-segment model fit, category gaps, scorecards, or distributions in a two-segment analysis. |

## Add a package

1. Create a folder under `chart-examples/` with a short, unique name describing the analytical use case.
2. Keep the plotting code and its README in that folder. Document the question the charts answer, required columns and grain, assumptions, dependencies, and how to run the examples.
3. Include a runnable example with synthetic data. Include rendered examples when they help readers inspect the result. Review chart labels, scales, captions, and interpretation alongside execution.
4. Add a row to this index. Future contributions can be discovered here with a single link from the main skill.

Keep any model-specific adapters optional and upstream of the skill. Pass analysis-ready data to the renderer and follow the skill’s validation, review, and evidence export.

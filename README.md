# Design Information Graphics

Use this skill with your coding assistant to create and refine a chart in your existing Python notebook or project.

## Make your first chart

1. Keep this folder together and make it accessible to the coding assistant you use with your project.
2. Open your notebook or Python project. Have an analysis-ready pandas DataFrame with the values you want to plot.
3. Paste the request below into your coding assistant’s chat. Replace the path, notebook name, and column names with yours.

> Read and follow `path/to/design-information-graphics/SKILL.md`. In `retention.ipynb`, use the DataFrame `retention_by_tenure` to show how 90-day retention varies by tenure group. It has one row per group, with `tenure_group` and `retention_rate` (a proportion from 0 to 1). The audience is the customer strategy team. Add the chart code to the notebook and show me a draft.

If the data still needs grouping, joins, or metric calculations, do that in your analysis first. Include any benchmarks or uncertainty values you want shown.

## Revise and save

- Give feedback in the same chat. For example, say **“Make the labels larger.”**
- When you’re ready to save, say **“Finalize this graph.”** The chart code stays in your notebook or Python project. The assistant saves the graph and a CSV of the exact data shown, with matching names such as `retention-by-tenure.png` and `retention-by-tenure.csv`.
- To return to a saved graph, say **“Revise retention-by-tenure.”** The next finalized version gets a suffix such as `-v02`, so you can keep both versions.

## For contributors

| Path | What belongs there |
| --- | --- |
| [SKILL.md](SKILL.md) | The workflow the assistant follows |
| [guides/](guides/) | Shared design and review guidance and instructions for specific chart types |
| [chart-tools/](chart-tools/) | Python helpers, styles, and templates |
| [chart-examples/](chart-examples/README.md) | Contributed chart packages with input requirements and runnable examples |

In your pull request, describe the behavior change and what you tested. Try a first graph with limited context and a second graph in the same project to check that the assistant reuses what it already knows. Record judgment-based feedback in the review ledger and link settled decisions to their pull requests.

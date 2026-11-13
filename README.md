# Design Information Graphics

Use this skill with your coding assistant to create and refine a chart in your existing Python notebook or project.

## Make your first chart

1. Keep this folder together and make it accessible to the coding assistant you use with your project.
2. Open your notebook or Python project. Have an analysis-ready pandas DataFrame with the values you want to plot.
3. Choose a prompt below and paste it into your coding assistant’s chat. Replace the path to `SKILL.md` with the one your assistant can access.

### For all charts in this session

Paste this at the start of the chat, then ask for each chart as you need it.

> Read and follow `path/to/design-information-graphics/SKILL.md` for all graphs and charts in this session.

### For one chart

Use this prompt when you want to apply the skill to a single chart. Replace the notebook, DataFrame, and column names with yours.

> Read and follow `path/to/design-information-graphics/SKILL.md`. In `retention.ipynb`, use the DataFrame `retention_by_tenure` to show how 90-day retention varies by tenure group. It has one row per group, with `tenure_group` and `retention_rate` (a proportion from 0 to 1). The audience is the customer strategy team. Add the chart code to the notebook and show me a draft.

If the data still needs grouping, joins, or metric calculations, do that in your analysis first. Include any benchmarks or uncertainty values you want shown.

## Use a PowerPoint brand template

1. In your working project, create `visualization/brands/<brand-id>/examples/`. Replace `<brand-id>` with a short name such as `acme`.
2. Drop your PowerPoint template or example deck there. You can include a brand guidelines PDF in the same folder.
3. Paste a request like this into your coding assistant’s chat. Replace the paths and brand name with yours.

> Read and follow `path/to/design-information-graphics/SKILL.md`. Use `visualization/brands/acme/examples/acme-template.pptx` to draft an Acme chart brand profile. Extract the fonts and colors defined in the PowerPoint theme, and flag any chart conventions you infer from the slides. Show me the draft for review.

After reviewing the draft, ask the assistant to save it as `visualization/brands/acme/brand-profile.yaml`. For future charts, say **“Use the Acme brand profile.”**

[Brand profile guide](guides/brand-profiles.md)

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

### Independent chart review

Start with a manual review on the team's private golden set. The skill library owns the shared review workflow, including what reviewers receive, how they report findings, and how revisions are routed. The visualization skill owns the chart criteria, including fit to the question, fidelity to the data, scales and encodings, and readability in the intended medium. The team owns the golden set and the final judgment.

1. **Generate a draft.** Give the visualization agent the request and inputs it would receive in normal use. Save the first chart.
2. **Review in a fresh chat.** Give an independent reviewer the original request, rendered chart, and source values needed to check it. Include code when checking reproducibility. Keep the golden-set expectations and the visualization agent's reasoning private during this review.
3. **Evaluate privately.** Compare the first chart and review against your golden-set expectations. In the review ledger, record chart defects, issues the reviewer missed, and findings it raised unnecessarily. Short judgment notes are fine.
4. **Revise and recheck.** Send actionable findings back to the visualization agent, have the reviewer check the revised chart, and record your verdict.

Use this prompt in the reviewer chat:

> Review this chart against the request and source values. Check whether it answers the question, represents the data faithfully, uses appropriate scales and encodings, and is readable in the intended medium. Give a **Pass** or **Revise** verdict. For each issue, identify the mark, label, or source value involved and suggest a concrete fix.

In routine use, the reviewer works from the request and chart evidence, and a human makes the final decision before stakeholder use. The golden set is reserved for offline evaluation of both the visualization agent and the reviewer.

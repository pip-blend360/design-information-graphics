---
name: design-information-graphics
description: Design, render, review, and revise rigorous static data graphics from analysis-ready in-memory pandas DataFrames in VS Code, notebooks, or Python IDEs. Use for selecting a graph format, creating explanatory or exploratory Matplotlib/Seaborn graphics, applying brand styles, exporting Excel-ready evidence CSVs, or improving existing Python visualizations. Do not use for data preparation, modeling, dashboards, or interactive graphics.
---

# Design Information Graphics

Create visual arguments whose form makes the intended evidence easy to see. Use Python as the renderer, accept only analysis-ready in-memory pandas DataFrames, and always preserve an Excel-ready export of the exact values used in the display.

## Route the request

Identify the mode: **create**, **review**, **refine**, **collection**, or **brand profile**.

Read only the guidance required for that mode:

- Always read [references/design-principles.md](references/design-principles.md).
- For any creation or material redesign, read [references/general-graph-guidance.md](references/general-graph-guidance.md).
- For creation, also read [references/intake-and-clarification.md](references/intake-and-clarification.md), [references/data-contracts.md](references/data-contracts.md), and [references/choosing-graph-format.md](references/choosing-graph-format.md).
- After choosing the format, read only its specialist reference:
  - Pie graph, divided-bar graph, or visual table: [references/pie-divided-bar-visual-tables.md](references/pie-divided-bar-visual-tables.md)
  - Bar graph, stacked-bar graph, step graph, or side-by-side bar graph: [references/bar-graph-variants.md](references/bar-graph-variants.md)
  - Line graph, layer graph, or scatterplot: [references/line-graph-variants-and-scatterplots.md](references/line-graph-variants-and-scatterplots.md)
- After the specialist reference, read [references/color-and-optional-components.md](references/color-and-optional-components.md) when the graphic uses color, texture, fills, gridlines, legends, captions, backgrounds, or multiple panels.
- For rendering or publishing, read [references/python-rendering.md](references/python-rendering.md).
- For review or refinement, read [references/review-and-iteration.md](references/review-and-iteration.md) and load the original brief and contract when available.
- For several graphics, also read [references/project-integration.md](references/project-integration.md).
- For brand work, also read [references/brand-profiles.md](references/brand-profiles.md).

## Enforce the boundaries

- Treat every source DataFrame as read-only.
- Never join, aggregate, reshape, impute, deduplicate, substantively filter, engineer features, define metrics, remove outliers, or fit models.
- Allow only presentation operations after validation: selecting used columns, setting visual order, formatting labels, calculating graphical coordinates, and making shallow copies.
- Require the DataFrame at the exact grain needed by each graphic or panel. If panels require different grains, require separately named, analysis-ready DataFrames.
- Do not load CSVs, spreadsheets, or databases. Standalone file-driven execution is out of scope.
- If meaning is ambiguous or validation fails, stop before constructing a figure or writing outputs. State the failed rule, expectation, observation, risk, and upstream correction.
- Never let a requested story outrun the evidence or silently overwrite an artifact.

## Workflow

1. Inspect the request, available DataFrame schema, project context, registry, brand examples, and prior outputs before asking questions.
2. Establish the audience, question or decision, explanatory or exploratory mode, intended comparison, primary-message status, artifact context, and constraints. Ask one consequential question at a time only when needed.
3. Assign a semantic lowercase-hyphenated `graphic_id`; keep it stable across revisions and increment the version.
4. Declare and validate the input contract before rendering.
5. Apply the shared perception and framework guidance.
6. Use the format-selection reference to choose the format from the reader's task, data relationship, and required precision. Do not begin with a preferred chart type.
7. Load the specialist reference for the selected format and construct the visual argument.
8. Apply the color and optional-components reference when relevant; treat it as a finishing layer, not a substitute for format-specific guidance.
9. Resolve style in this order: creator-approved override, project standards, brand profile, skill defaults. Report unavailable fonts and use an approved or reasonable fallback; never redistribute fonts.
10. Write reusable Matplotlib/Seaborn code that accepts the validated DataFrame and returns a `matplotlib.figure.Figure` without saving or calling `plt.show()`.
11. Publish versioned PNG and SVG outputs plus Excel-ready evidence CSV file(s) and metadata. Use one CSV when all visible evidence has one grain; use separate clearly named CSVs when panels use different grains. Each CSV must contain every value used for marks, labels, benchmarks, intervals, sample sizes, and factual annotations, with no styling instructions or unrelated columns.
12. Review fidelity, integrity, hierarchy, annotations, clipping, spacing, and collection consistency. Repair only low-risk presentation defects automatically.

## Integrity precedence

Perceptual guidance serves truthful communication. If a brand convention, requested format, or book-derived heuristic would distort proportion, hide uncertainty, imply unsupported causality, or weaken reproducibility, preserve graphical integrity and document the departure.

## Complete handoff

Return the PNG, SVG, reusable plotting source, evidence CSV file(s), metadata with evidence fingerprint(s), brief, input contract, concise rationale, assumptions, and unresolved limitations. For revisions, also return the updated feedback and version record.

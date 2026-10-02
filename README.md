# Design Information Graphics

One portable AI skill for designing, rendering, reviewing, and refining narrative information graphics in a scientist's existing notebook or Python package.

## Architecture and components

The scientist invokes `design-information-graphics`. One coordinator manages the sequence and loads only the supporting modules needed for the current graph. Modules are reference files within this skill, not independently installed skills.

| Component | Responsibility | Location |
| --- | --- | --- |
| Coordinator | Control the sequence, reuse project context, route to modules, and recognize finalization | `SKILL.md` |
| Brainstorming/intake | Establish audience, medium, purpose, and consequential uncertainties | `references/intake-and-clarification.md` |
| Format selection | Choose a graph from the communication goal and data structure | `references/format-selection.md` |
| Graph-format modules | Guide proportions; quantitative comparisons and ranking; lines and scatter plots; stacked compositions and cumulative totals; special cases | Five graph-family files in `references/` |
| Shared guidance | Apply design principles, data contracts, narrative composition, branding, Python rendering, project consistency, and review | Existing files in `references/` |
| Execution helpers and assets | Validate inputs, export graph data, and supply styles and templates | `resources/` |
| Collaborator guide | Explain architecture, usage, and contributions | `README.md` |

### Implementation status

The coordinator, lightweight intake, format selector, five graph-family modules, iteration/finalization guidance, and graph/CSV exporter are implemented. Common charts use Matplotlib and Seaborn with analysis-ready pandas DataFrames. Special cases are conditional on supplied structures and available Python tools; the module defines requirements and alternatives rather than guaranteeing every diagram.

### Existing supporting files

`references/` contains `design-principles.md`, `intake-and-clarification.md`, `data-contracts.md`, `narrative-composition.md`, `python-rendering.md`, `brand-profiles.md`, `project-integration.md`, and `review-and-iteration.md`.

`references/` also contains `format-selection.md`, `proportions.md`, `quantitative-and-ranking.md`, `lines-and-scatter.md`, `composition-and-cumulative.md`, and `special-cases.md`.

`resources/` contains `validation.py`, `export_bundle.py`, `information-graphic.mplstyle`, `default-palette.json`, and `brand-profile-template.yaml`.

## Use and workflow

Keep `SKILL.md`, `references/`, and `resources/` together. Point your coding assistant to `SKILL.md`, or place the complete folder in your environment's supported skill location. No particular coding harness is required.

Provide the graph objective and analysis-ready input data. Treat source data as read-only; upstream analysis supplies the required grain and metrics.

1. **Establish context briefly.** Reuse audience, medium, brand, and conventions across the project. Infer a brief when the request is clear; ask only when an answer could materially change interpretation or design.
2. **Choose the format.** Select it from the intended relationship and data structure, explain the choice briefly, and load the relevant format module. Respect an explicitly requested format and suggest an alternative when there is a concrete reason.
3. **Render and iterate.** Show a draft in the existing notebook or Python environment. Accept ordinary feedback such as "make the labels larger" or "try a line chart." Revise the same graph without repeating intake; revisit only decisions affected by the feedback.
4. **Finalize.** When the scientist says **"finalize this graph,"** apply any accompanying last instruction, run final checks, and export the deliverables. Resolve consequential ambiguity or validation failure before finalizing.

Finalization applies only to the current graph. "Looks good" is conversational feedback; the explicit phrase marks completion. For example: "Finalize this graph with the larger title." Show previews during drafting and export final deliverables at finalization, or earlier if requested.

## Graph identity and revisions

The assistant chooses a stable, descriptive graph ID and checks for collisions. Use it for the notebook section and matching exports, such as `retention-by-tenure.png` and `retention-by-tenure.csv`.

To reopen a finalized graph, say **"Revise retention-by-tenure."** Keep its ID, preserve prior exports, and give the next finalized version matching suffixes, such as `retention-by-tenure-v02.png` and `retention-by-tenure-v02.csv`. Keep reproducible code for retained versions through existing notebook or package version history, or an identifiable saved code version.

## Final handoff and evidence

Each finalized graph has three deliverables:

1. The graph.
2. Its code in the notebook or Python package already in use.
3. The exact graph data as a CSV, suitable for recreation in Excel or another tool.

The CSV is the evidence artifact. Include category labels, plotted values, and values used for benchmarks, error bars, or factual annotations. Preserve numeric precision, make units clear, and regenerate the CSV when a revision changes the data shown. Export it locally beside the graph using the matching graph ID; upload or share externally only when requested.

Keep essential source and interpretation notes beside the graph in the notebook. Do not require separate per-graph YAML files, briefs, evidence reports, or tracking documents. Record reusable project context and each graph's identity and draft/finalized status lightly in the existing notebook or project.

## Migration from the previous structure

Keep `references/`. Move the contents of `scripts/` and `assets/` into `resources/`, and update helper paths accordingly. Omit the optional OpenAI interface metadata in `agents/openai.yaml` from the portable distribution. Remove the old empty folders after moving their contents. This migration changes the skill package, not the scientist's project layout.

## Collaboration

Propose changes through pull requests, describing the intended behavior change and regression cases tested. Keep shared rules in the coordinator or shared references, and keep format modules focused on format-specific guidance. Update routing and file references whenever modules move or are added.

Test both a first graph with incomplete context and a later graph in the same project; the later graph should avoid repeating intake. Track judgment-based feedback in the review ledger, link settled decisions to pull requests, and tag tested versions.

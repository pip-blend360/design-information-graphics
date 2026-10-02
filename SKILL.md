---
name: design-information-graphics
description: Design, render, review, and iterate static information graphics in an existing Python notebook or package. Use for graph brainstorming, selecting formats, proportions, categorical comparisons and ranking, lines and scatterplots, stacked compositions and cumulative totals, and supported sets, hierarchies, maps, diagrams, and flows. Reuse project context across graphs. Require analysis-ready read-only inputs; do not prepare data, define metrics, aggregate, join, impute, fit models, or create dashboards.
---

# Design Information Graphics

Coordinate one skill with supporting modules. Use Python to render; preserve quantitative integrity and integrate code into the scientist's existing notebook or package.

## Load guidance selectively

Read `references/design-principles.md` and `references/intake-and-clarification.md` for new graphs, reusing already loaded guidance and established context. Read `references/format-selection.md`, then only the selected family:

- `references/proportions.md`
- `references/quantitative-and-ranking.md`
- `references/lines-and-scatter.md`
- `references/composition-and-cumulative.md`
- `references/special-cases.md`

For rendering, read `references/data-contracts.md`, `references/narrative-composition.md`, and `references/python-rendering.md`. For feedback and finalization, read `references/review-and-iteration.md`. Read `references/project-integration.md` for shared project context and `references/brand-profiles.md` when resolving branding. Do not reload unaffected modules on every revision.

## Protect boundaries

Treat source inputs as read-only. Never join, aggregate, reshape analytically, impute, deduplicate, substantively filter, engineer features, define metrics, remove outliers, or fit models. Allow presentation-only column selection, ordering, label formatting, shallow copies, and graphical coordinates. Require the exact analytical grain and all displayed values upstream. Never guess denominators or silently coerce values. Validate before figures or exports; report actionable failures without fixing data. Do not let narrative claims outrun evidence.

## Coordinate the workflow

1. **Brainstorm briefly.** Inspect the request, existing code, data schema, and project notes. Reuse audience, medium, brand, and conventions. Infer a compact working brief when clear; ask one focused question only when uncertainty could materially change interpretation or design. Keep context in the existing notebook/project, not separate per-graph briefs or YAML.
2. **Choose the format.** Use the format selector and the relevant family module. Explain the choice briefly. Respect requested formats; explain a concrete mismatch and propose an alternative when necessary. Reuse an existing choice on cosmetic revisions.
3. **Assign identity and validate.** Choose a descriptive lowercase hyphenated `graphic_id`, check existing headings, functions, and files for collisions, and keep it stable across revisions. Distinguish a new graph from reopening one. Establish grain, fields, units, semantics, uniqueness, and missing-value policy in code or nearby notes. Use `resources/validation.py` when suitable; special structures need explicit equivalent checks.
4. **Design and render a draft.** Compose the comparison, labels, annotations, and necessary qualifications. Apply creator overrides, project standards, brand profile, then defaults. Integrate runnable code into the existing notebook/package; show the graph there. Use Matplotlib and Seaborn where suitable. Do not silently add dependencies or create a replacement notebook when the original is available. Keep previews lightweight and avoid permanent exports until requested.
5. **Iterate.** Apply ordinary feedback to the same graph. User-requested design changes are authorized; ask only about consequential ambiguity, conflicting requests, unsupported inputs, or misleading implications. Revisit the selector or data checks only when affected. Do not force another brainstorming session, approval gate, or feedback ledger.
6. **Finalize on instruction.** Recognize **"finalize this graph"** as completion for the current graph. Apply accompanying last edits, check fidelity and rendered layout, then save the graph and exact data CSV. "Looks good" alone remains feedback; explicit equivalent instructions to finalize or export are also sufficient. Do not finalize with validation failures or unresolved material ambiguity.
7. **Reopen safely.** On "Revise <graphic_id>", retain the ID and prior exports. Save the next finalized version with matching suffixes such as `-v02`. Preserve code for retained versions in available version history or an identifiable saved code version. Never silently overwrite final exports.

## Deliver exactly three items

- The graph: display it in the notebook and save PNG by default; use SVG or another appropriate format when requested or required by the medium.
- The graph code in the notebook or Python package already in use. If inaccessible, supply ready-to-insert code and state that integration remains pending.
- The exact graph data as a CSV beside the saved graph, with matching ID/version. Include all labels, plotted values, uncertainty, benchmarks, and factual annotation values; preserve precision and meaningful identifiers. Never export unrelated source columns or an internal index.

Use `resources/export_bundle.py` for local graph and CSV exports when suitable. Keep essential source, units, and interpretation notes beside the graph. Do not require metadata YAML, separate briefs, evidence reports, registries, or standalone source files when code is already integrated. Local export is evidence publication; external upload or sharing requires a request.

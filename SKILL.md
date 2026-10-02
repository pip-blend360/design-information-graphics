---
name: design-information-graphics
description: Design, render, review, and revise rigorous narrative information graphics from analysis-ready pandas DataFrames in Jupyter notebooks or Python IDEs. Use for creating explanatory or exploratory static data graphics, improving existing Python visualizations, coordinating multiple graphics in a larger data-science project, applying or inferring brand styles from examples, exporting publication artifacts, or incorporating creator and stakeholder feedback. Requires read-only, contract-valid input data and renders with Matplotlib or Seaborn; do not use for data preparation, aggregation, joins, imputation, modeling, dashboards, or interactive graphics.
---

# Design Information Graphics

Create evidence-led visual explanations that combine the narrative coherence of an infographic with quantitative integrity. Treat words, numbers, annotations, and graphical marks as one composition. Use Python as the only renderer.

## Route the request

Identify the mode before acting:

- **Create**: Design a new information graphic from an in-memory pandas DataFrame.
- **Review**: Evaluate an existing graphic, figure, notebook cell, or plotting function.
- **Refine**: Revise an existing graphic from creator or external feedback.
- **Collection**: Plan or harmonize several graphics within one analytical project.
- **Brand profile**: Infer or apply a reusable visual system from supplied examples.

Read only the references required for the mode:

- Always read `references/design-principles.md`.
- For creation, read `references/intake-and-clarification.md`, `references/data-contracts.md`, `references/narrative-composition.md`, and `references/python-rendering.md`.
- For review or refinement, read `references/review-and-iteration.md` plus the original brief and contract when available.
- For several graphics, also read `references/project-integration.md`.
- For brand work, also read `references/brand-profiles.md`.

## Enforce non-negotiable boundaries

- Treat every source DataFrame as read-only.
- Never join, aggregate, reshape, impute, deduplicate, filter substantively, engineer features, define metrics, remove outliers, or fit models.
- Never silently coerce incompatible values or guess metric semantics.
- Allow only presentation operations after validation: select used columns, set visual order, format labels, calculate graphical coordinates, and make a shallow copy.
- Require an analysis-ready DataFrame at the exact grain needed by the graphic.
- If data meaning is ambiguous, ask one focused question at a time.
- If structure or values violate the declared contract, raise an actionable error and create no outputs.
- Never let a requested story outrun the evidence.
- Do not silently overwrite an existing graphic, CSV, SVG, PNG, or metadata file.

## Follow the workflow

### 1. Inspect context before questioning

Inspect the request, named DataFrame schema, existing project files, graphic registry, brand examples, and earlier graphic artifacts. Do not repeat questions already answered by available context.

### 2. Reach a decision-ready brief

Determine the audience, communication objective, exploratory or explanatory mode, intended decision, evidence, primary message status, artifact context, and constraints. Ask one consequential question at a time. Infer harmless implementation details and state them briefly.

Do not render until no unresolved decision could materially change the analytical interpretation or design. For complex work, summarize the brief before proceeding.

### 3. Assign a stable identity

Create a semantic lowercase hyphenated `graphic_id`, such as `retention-program-effect`. Check the project registry before accepting it. Keep the ID stable across revisions; increment the version. Use a different ID for a materially different graphic. Never use generic IDs such as `chart-1`.

### 4. Declare and validate the data contract

Document the DataFrame name, grain, required fields, semantic meanings, types, units, null policy, bounds, expected categories, and uniqueness keys. Use `resources/validation.py` when helpful.

Stop when the contract is incomplete or validation fails. State what was expected, what was observed, why rendering is blocked, and what the upstream workflow must provide. Do not fix the data.

### 5. Design the visual argument

Identify the comparisons and evidence that matter. Choose graphical forms based on relationships, not software defaults. Compose a headline, primary display, supporting evidence, annotations, benchmarks, units, source notes, and methodological qualifications as needed. Prefer direct labels and meaningful comparisons. Use design restraint without equating rigor with empty minimalism.

### 6. Apply project and brand context

Resolve style in this order:

1. Creator-approved graphic override
2. Project visualization standards
3. Selected brand profile
4. Skill defaults

When examples are supplied, infer a candidate brand profile, separate verified properties from uncertain inferences, and ask for confirmation where uncertainty changes the result. Never download or redistribute fonts. If an identified font is unavailable, report it and propose a fallback.

### 7. Render in Python

Use Matplotlib for composition and Seaborn for appropriate statistical marks. Accept an existing pandas DataFrame and return a `matplotlib.figure.Figure`. Avoid hidden notebook state and `inplace=True`. Keep saving separate from figure construction. Do not call `plt.show()` inside reusable functions unless the user requests it.

Render PNG and SVG outputs. Use the same stable filename stem as the `graphic_id`, with version suffixes when needed.

### 8. Publish the evidence bundle

Export the minimum evidence CSV containing every value needed to reproduce visible marks and factual annotations, and no unrelated columns. Select columns from the same validated DataFrame used by the renderer; do not construct a separate analytical dataset.

Write metadata YAML containing the graphic ID, version, title, source DataFrame, grain, filenames, field list, brand profile and version if used, generation time, and SHA-256 fingerprint of the evidence CSV. Use `resources/export_bundle.py` when helpful.

Produce no partial bundle after a validation failure. Never overwrite an existing bundle without explicit authorization.

### 9. Review and iterate

Check data fidelity, graphical integrity, narrative coherence, visual hierarchy, annotations, clipping, spacing, and consistency with the project collection. Automatically repair only low-risk presentation defects. Ask before changing the message, comparison, scale interpretation, data contract, or audience objective.

For external feedback, load the saved brief, contract, code, metadata, and feedback history. Classify each comment as accepted, clarification needed, conflicting, out of scope, upstream-data work, or potentially misleading. Record the disposition and rationale. Save a new version rather than overwriting the prior one.

## Return a complete handoff

Return:

- The rendered PNG and SVG
- The Matplotlib `Figure` or reusable plotting function
- Reproducible Python source
- The minimum-data evidence CSV
- Metadata YAML with the evidence fingerprint
- The brief and input contract
- A concise design rationale, assumptions, and unresolved limitations
- Updated feedback and version records when revising

Adapt to an existing project layout. Do not force a heavyweight folder structure into a small notebook, but preserve the same logical artifacts.

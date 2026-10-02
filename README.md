# Design Information Graphics

A portable AI skill for designing, rendering, reviewing, and refining narrative information graphics from analysis-ready pandas DataFrames using Matplotlib and Seaborn.

## Directory structure

The skill uses two supporting folders. Paths are relative to the repository root.

| Location | Purpose |
| --- | --- |
| `SKILL.md` | Skill entry point, workflow, boundaries, and reference routing |
| `references/` | Design and workflow guidance, read as needed |
| `resources/` | Python helpers, rendering style, palette, and brand template |
| `README.md` | Repository overview for collaborators |

### References

- `design-principles.md`: visual and quantitative design principles
- `intake-and-clarification.md`: establish the brief and resolve consequential questions
- `data-contracts.md`: declare and validate analysis-ready inputs
- `narrative-composition.md`: compose the visual argument
- `python-rendering.md`: build reproducible Python graphics
- `brand-profiles.md`: infer and apply brand styles
- `project-integration.md`: coordinate graphics within a project
- `review-and-iteration.md`: review outputs and incorporate feedback

### Resources

- `validation.py`: input contract validation helper
- `export_bundle.py`: evidence bundle export helper
- `information-graphic.mplstyle`: Matplotlib style defaults
- `default-palette.json`: default color palette
- `brand-profile-template.yaml`: reusable brand profile template

## Use

Keep `SKILL.md`, `references/`, and `resources/` together. Point your coding assistant to `SKILL.md`, or place the complete folder in the skill location supported by your environment. The assistant should load supporting references according to the routing instructions in `SKILL.md`. This repository does not require a particular coding harness.

Provide an analysis-ready pandas DataFrame and the graphic objective. The skill treats source data as read-only; upstream analysis must supply the required grain and metrics. Deliverables include rendered graphics, reproducible Python source, an evidence CSV, metadata, and the brief and contract.

## Migration from the previous structure

- Keep `references/` and its filenames.
- Move the contents of `scripts/` and `assets/` into `resources/`.
- Update helper paths to `resources/validation.py` and `resources/export_bundle.py`.
- Omit `agents/openai.yaml` from the portable distribution. It contains optional OpenAI interface metadata.
- Remove the old empty folders after moving their contents.

This change simplifies the skill package. It does not change the layout of projects or output bundles created with the skill.

## Collaboration

Propose changes through pull requests. Describe the intended behavior change and the regression cases tested. Keep the skill entry point and resource paths consistent when moving files. Track judgment-based feedback in the review ledger and link settled decisions to the relevant pull request. Tag tested versions so results can be traced to a specific revision.

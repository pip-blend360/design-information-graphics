# Design Information Graphics

This repository contains one harness-neutral visualization skill for coding
environments with an analysis-ready in-memory pandas DataFrame.

## Repository layout

```text
design-information-graphics/
├── AGENTS.md
├── CLAUDE.md
└── skills/
    └── design-information-graphics/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

`skills/design-information-graphics/` is the canonical, portable unit. Its
instructions do not depend on Copilot, Claude, Codex, or another named harness.
Root discovery files only tell coding agents where that skill lives.

## Use in a data-science repository

Copy this structure into the root of the repository, or add this repository as
a submodule and point the repository's root agent instructions to the canonical
`SKILL.md`.

Then ask the coding assistant to use the design-information-graphics skill and
name the prepared DataFrame, audience, decision, and intended message. The
assistant generates reusable plotting and publishing code. Run that code in the
notebook or Python session that owns the DataFrame.

The expected handoff includes Python source, PNG, SVG, metadata, and the exact
Excel-ready evidence CSV file or files used by the visual.

# Repository agent guidance

Reusable AI skills live under `skills/`. For any request to select, create,
review, or refine a static data visualization, read and follow
`skills/design-information-graphics/SKILL.md` before acting. Load only the
supporting references that `SKILL.md` routes to.

The data-science project owns analysis and preparation. Treat named in-memory
DataFrames as read-only and generate code for execution in the environment that
owns the live DataFrame.

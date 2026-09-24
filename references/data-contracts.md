# Data Contracts

Understand data sufficiently to visualize it truthfully. Do not prepare, redefine, or analytically transform it. Require an analysis-ready pandas DataFrame at the exact grain needed by the graphic.

Record the DataFrame variable, grain and uniqueness key, required fields, business meanings, semantic types, units, null policies, valid bounds, and expected categories or ordering.

```yaml
dataframe: retention_summary
grain: one row per month and cohort
unique_by: [month, cohort]
fields:
  month: {semantic_type: datetime, role: time, nullable: false}
  cohort: {semantic_type: category, role: series, nullable: false}
  retention_rate:
    semantic_type: numeric
    role: measure
    unit: proportion
    minimum: 0
    maximum: 1
    nullable: false
```

Do not automatically aggregate duplicate grain, parse ambiguous dates, convert percentages, remove nulls, fill values, or filter categories. An actionable error must state the failed rule, expectation, observation, reason rendering is blocked, and required upstream correction. Fail before creating any figure or output.

The evidence CSV must contain values encoded by position, length, area, color, or shape; group and facet IDs; label values; uncertainty bounds; displayed sample sizes; and benchmark values. Exclude unused columns and internal indexes. Use the same validated DataFrame for rendering and export.

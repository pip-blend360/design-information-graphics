# Choosing a Graph Format

Choose the format from the reader's task, the semantic relationship in the validated data, and the required precision. This reference synthesizes Chapter 2 of Stephen M. Kosslyn's *Graph Design for the Eye and Mind* (2006), with integrity constraints for modern analytical graphics.

## Decide whether a graph is appropriate

- Use a graph when the reader must perceive relative amounts, patterns, trends, distributions, composition, or association.
- Use a conventional table when exact lookup of many individual values is the primary task.
- Use a visual table when the goal is a quick impression of rank or relative quantity and pictorial or repeated marks genuinely aid recognition.
- Formulate the reader's question before selecting a format. Include the data needed to answer it and no unrelated series.

## Selection sequence

1. Identify the relationship: exact lookup, part-to-whole, discrete comparison, change over a continuous variable, paired contrast, association, cumulative total, or multi-panel comparison.
2. Identify the task: approximate impression, precise value recovery, ranking, change, interaction, exception, uncertainty, or comparison of specified cases.
3. Check the field semantics: nominal, ordinal, interval/continuous, time, measure, proportion, uncertainty, and grouping variables.
4. Choose the simplest familiar format that supports the task without requiring mental subtraction, legend lookup, or unsupported inference.
5. Reject any candidate whose encoding is incompatible with the data or required precision.

## Format decision table

| Reader task and data relationship | Prefer | Avoid or qualify |
| --- | --- | --- |
| Exact lookup of many values | Conventional table | A graph that forces visual estimation |
| Approximate parts of one meaningful whole | Pie graph | Multiple pies with substantially different compositions; precise comparisons |
| More accurate parts of one whole, or comparison of several 100% wholes | Divided-bar graph | Too many small segments or tasks requiring repeated mental subtraction |
| Quick rank or relative-amount impression using recognizable marks | Visual table | Scaling both height and width; decorative icons unrelated to the variable |
| Discrete point values or category magnitudes | Bar graph | A line joining nominal categories |
| Change over time or another interval variable | Line graph | Unequal intervals shown at equal spacing; lines over unordered categories |
| Interaction or contrasting trends | Multiple lines or small multiples | Mixed bar/line encodings for the interaction |
| Specific paired comparisons between two conditions | Side-by-side bars or a two-point line graph | More than two crowded comparison series |
| Overall association between two quantitative variables | Scatterplot | Extra encodings that obscure the relationship; causal language without design support |
| Components of totals across nominal cases | Stacked bars | Precise comparison of interior segments without a common baseline |
| Components of a total changing over continuous X | Layer/area graph | Precise component values or a nominal X axis |
| Many series or separate comparison questions | Small multiples | A single overloaded panel |

## Rules for Chapter 4 formats

Choose a **pie graph** only when all are true:

- The values are nonnegative parts of one meaningful whole.
- The total and denominator are unambiguous.
- The reader needs approximate relative shares, not fine comparisons or exact lookup.
- The category count and labels remain legible as a small number of perceptual units.

Choose a **divided-bar graph** when:

- Values are nonnegative components of a meaningful 100% whole.
- Segment length will communicate shares more accurately than angle or area.
- One or several wholes must be compared with a consistent category order.

Choose a **visual table** when:

- The intended message is rank or approximate relative amount.
- A repeated symbol, common-baseline extent, or directly comparable mark is compatible with the subject.
- It reduces reading effort rather than acting as decoration.

After selecting any of these formats, read [pie-divided-bar-visual-tables.md](pie-divided-bar-visual-tables.md).

Choose a **bar-graph variant** for discrete magnitudes, grouped category comparisons, changing totals split into components, discrete steps, or direct paired comparisons. After selection, read [bar-graph-variants.md](bar-graph-variants.md).

Choose a **line-graph variant or scatterplot** for change over a true interval variable, interactions, continuous part-to-whole change, or association between two quantitative measures. After selection, read [line-graph-variants-and-scatterplots.md](line-graph-variants-and-scatterplots.md).

## Complexity and optional features

- Treat four simultaneous perceptual units as a warning threshold. Count grouped patterns, not raw marks. Use small multiples when the display cannot be understood at a glance.
- Put series that must be compared in the same panel when that comparison remains legible; separate unrelated questions into different panels.
- Prefer direct labels. Use a key only when direct labels would be unreadable or when the same mapping repeats across several panels.
- Include uncertainty when it changes how the comparison should be interpreted and the source DataFrame supplies it.
- Add gridlines when precise extraction matters; otherwise use only enough guides for orientation.
- Plot two dependent measures together only when their relationship is central and the association between each measure and its scale is unmistakable. Otherwise use aligned panels.
- Add a caption or nearby note for unfamiliar terminology, nonstandard encodings, or necessary qualifications.

After applying the chosen specialist reference, use [color-and-optional-components.md](color-and-optional-components.md) whenever optional finishing components or multiple panels are involved.

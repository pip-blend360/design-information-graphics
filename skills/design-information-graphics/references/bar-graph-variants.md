# Bar-Graph Variants

Read this only after [choosing-graph-format.md](choosing-graph-format.md) selects a bar graph, stacked-bar graph, step graph, or side-by-side bar graph. It synthesizes Chapter 5 of Stephen M. Kosslyn's *Graph Design for the Eye and Mind* (2006), adapted for static Python output, truthful scales, and Excel-ready evidence export.

## Shared bar rules

- Use bar extent to encode amount and start the magnitude scale at a meaningful zero. If the analytical question is deviation from a nonzero benchmark, encode the deviation explicitly rather than truncating an ordinary magnitude bar.
- Draw complete, easily detected bars. Do not remove useful structure merely to maximize a data-ink ratio; every line or fill must either encode data, clarify grouping, or support accurate reading.
- Keep corresponding series in the same order and give them the same appearance in every cluster and panel.
- Use emphasis only when a specific bar is central to the supported message. Otherwise keep equal-role bars equally salient.
- Keep every bar within the visible scale when readers need values. Never let clipping or overflow imply an unbounded amount.
- Prefer direct or hierarchical labels over a legend. Use consistent terminology and label hierarchy for nested variables.
- Display source-provided uncertainty only when its meaning is declared. Show the supplied lower and upper bounds faithfully; do not calculate or discard an interval merely to simplify the mark.

## Grouped and ordinary bars

- Place intended comparisons adjacent.
- Leave noticeably more space between clusters than between bars within a cluster so proximity expresses the grouping.
- Do not overlap bars by default. If overlap is unavoidable, ensure both baselines and extents remain visible and the result cannot be mistaken for stacking.
- Keep bar widths consistent unless width intentionally encodes a declared quantity. Ordinary bar width must not imply another measure.
- Use horizontal bars when labels are long or the task benefits from aligned text. Retain a common zero baseline and natural reading order.
- Order nominal categories by the message: intended pairs together, a meaningful convention, or a simple value progression. Do not alphabetize by habit.

## Stacked bars

- Use stacked bars only for components of totals that vary across nominal or ordinal cases.
- Keep the segment order and semantic colors identical across bars.
- When no semantic order governs, place the component that changes least at the common baseline. This gives the remaining boundaries a more stable comparison base.
- Make the total and the contribution of each segment unambiguous. Include total labels only when they serve the question.
- If precise comparison of interior segments is central, choose grouped bars, aligned dots, small multiples, or another common-baseline format.
- Do not confuse stacked bars with divided bars: stacked-bar totals vary; divided bars represent a constant 100% whole.

## Step graphs

- Use a step graph for one measure that changes in discrete intervals and when the duration or interval structure is meaningful.
- Make the step line at least as detectable as the framework and use equal visual widths only when the underlying intervals are equal. For unequal intervals, preserve their true positions and widths.
- A single restrained fill beneath the step line may help the pattern cohere. Do not alternate fills unless the alternation encodes a real variable.
- Label or annotate discontinuities only when they matter to the communication objective.
- Reject a step graph when its flat segments would falsely imply persistence between observations.

## Side-by-side bar graphs

- Use a side-by-side layout for direct comparison of two opposing or paired sets.
- Align corresponding bars on one central baseline or on precisely matched baselines so equal lengths mean equal values.
- Keep one consistent label side and align every label with its pair.
- If the nominal cases have no fixed order, sort one side into a simple progression so differences or reversals on the other side become visible.
- Avoid this format for more than two principal comparison series; use small multiples or another format when pair structure breaks down.

## Rendering and evidence checks

- Confirm that bar geometry uses validated values without hidden normalization.
- Confirm zero, units, denominators, category order, series order, interval bounds, totals, and annotations against the evidence CSV.
- Inspect cluster spacing, bar labels, and caps at final output size.
- Verify that the same category has the same treatment across clusters and panels.


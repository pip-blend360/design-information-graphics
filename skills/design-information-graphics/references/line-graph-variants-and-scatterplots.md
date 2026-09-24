# Line-Graph Variants and Scatterplots

Read this only after [choosing-graph-format.md](choosing-graph-format.md) selects a line graph, layer graph, or scatterplot. It synthesizes Chapter 6 of Stephen M. Kosslyn's *Graph Design for the Eye and Mind* (2006), adapted for static Python output and the skill's no-analysis boundary.

## Line graphs

- Use a line only when the horizontal variable has meaningful order and interval structure, usually time or another continuous measure. Preserve true spacing between observations.
- Make the focal line most salient only when the brief supports that emphasis. Keep equal-role lines equally prominent and move comparison lines into the background without making them unreadable.
- Ensure nearby and crossing lines remain distinguishable at final size and in grayscale. Prefer a small set of distinct colors plus line styles or point symbols rather than many subtly different hues.
- When dash patterns distinguish lines, make their frequencies substantially different; Kosslyn's practical threshold is approximately 2:1.
- When observed points are important, make markers clearly larger than the connecting line and use discriminable shapes. Do not rely only on filled versus hollow versions of the same small symbol.
- Do not fill the region between independent lines merely to emphasize their difference; it can dominate the chart or falsely imply a cumulative layer. Fill only when the band has a declared meaning such as a supplied interval.
- Show source-provided uncertainty faithfully and keep it visually associated with its series. Reduce opacity or weight to avoid turning the least precise series into the most salient one.
- Put direct labels in one consistent, uncluttered region, preferably at line ends. Use proximity and continuation to make each association obvious.
- Label only critical point values needed by the message. Export every labeled value.
- Avoid mixed line-and-bar displays for interactions. If two tightly related measures genuinely require different forms, establish one primary reading path and make every scale association explicit; aligned panels are usually safer.

## Layer graphs

- Use a layer graph only for components of a total changing over a continuous horizontal variable.
- Fill the layers so the display cannot be mistaken for several independent lines.
- Keep category order and appearance stable across the full domain.
- When no semantic order governs, place the least-changing component at the common baseline to improve comparison of boundaries.
- Use this format for overall composition and change, not precise interior component values. Choose aligned panels or lines when component precision is central.
- Verify that the top boundary equals the declared total at every horizontal position; require upstream correction if it does not.

## Scatterplots

- Use a scatterplot to show the overall association, clusters, gaps, and unusual observations between two quantitative fields. Do not imply causality without supporting design and analysis.
- Keep point symbols visible but small enough to reveal density. Use transparency for overplotting when it does not hide important small groups.
- If color or shape identifies groups, make symbols discriminable after reduction and in grayscale. Avoid confusable letters and tiny filled/hollow variants.
- Do not jitter, bin, aggregate, count overlaps, or otherwise alter point locations inside this skill. If multiplicity must be encoded by size, require upstream overlap counts and a declared size mapping.
- Use no more than a few clearly distinct size levels when size is supplied; area must be scaled to the quantitative value, and the evidence CSV must include the encoded size field.
- Keep uncertainty marks lighter than the points and ensure they do not make less reliable observations appear more important.
- A fitted or smoothed line is an analytical result. Never fit it in this visualization skill. Require upstream fitted values, intervals, model scope, and method label, then render them from the validated DataFrame.
- Make supplied fit lines visible, distinguish multiple fits clearly, label them directly, and state the fitting method in a nearby note or metadata.
- Do not connect observations unless sequence or another relationship makes the connection meaningful.

## Rendering and evidence checks

- Verify horizontal spacing, point coordinates, line endpoints, missing intervals, uncertainty bounds, group encodings, fitted values, and annotations against validated evidence.
- Confirm that visual emphasis follows the brief and does not conceal variability or outliers.
- Inspect crossings, labels, markers, transparency, and dense regions at final size.
- Export all observed coordinates and every supplied value used for lines, bands, fits, labels, benchmarks, and annotations.


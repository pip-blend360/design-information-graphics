# Pie Graphs, Divided-Bar Graphs, and Visual Tables

Read this only after [choosing-graph-format.md](choosing-graph-format.md) selects one of these formats. It synthesizes Chapter 4 of Stephen M. Kosslyn's *Graph Design for the Eye and Mind* (2006), adapted for static Python output and Excel-ready evidence export.

## Shared checks

- Validate that parts are nonnegative and that the denominator and whole are meaningful.
- Do not calculate, normalize, aggregate, or repair shares inside the visualization skill. Require analysis-ready values upstream.
- Keep category order, wording, and color meaning consistent between marks, labels, CSV evidence, and metadata.
- Prefer direct labels and include the displayed value when it aids reconstruction or interpretation.
- Export each component value, category, whole/facet identifier, displayed label value, benchmark, and annotation value used by the graphic.

## Pie graph

Use a pie to communicate approximate shares of one whole.

- Draw every wedge from the exact center so angle, arc, and area remain mutually consistent.
- Use no radial scale or grid.
- Honor a meaningful conventional or narrative category order when one exists. Otherwise arrange wedges in a simple progression, placing adjacent similar shares together; a practical default is ascending clockwise from 12 o'clock.
- If one slice is the explicit focus, place it near 12 o'clock when compatible with the chosen order and use restrained emphasis.
- Explode slices only when separation carries an explicit emphasis role. Explode at most a small minority of slices; Kosslyn's rough ceiling is one quarter of the wedges. Usually one emphasized slice is clearer.
- Put labels inside wedges only when every label remains comfortably legible. If they do not all fit, place all labels outside rather than mixing inside and outside placement without meaning.
- Keep leader lines short, unambiguous, and noncrossing. If labels or slices become crowded, reject the pie and select a more suitable format.
- Do not use multiple pies when substantially different compositions must be compared precisely. Prefer divided bars, aligned bars/dots, or another common-baseline display.

## Divided-bar graph

Use a divided bar to show components of one or more 100% wholes with length-based comparison.

- Fix every complete bar to the same 0–100% extent and state the unit as percent or proportion.
- Make bars wide enough for segments to be clearly distinct and, when possible, for direct labels to fit.
- Separate segments with parallel boundaries perpendicular to the bar. Sloped boundaries falsely suggest continuous change.
- For a single bar, a scale may share its left border. For multiple bars, place one common scale outside the set so it does not appear to belong only to the first bar.
- Keep segment order consistent across bars. When no semantic order governs, place the least-changing component at the common baseline so changes in other components are easier to compare.
- Directly label sufficiently large segments. Apply one consistent alternative for small segments rather than changing label position arbitrarily.
- If precise comparison of multiple interior segments is central, use a different common-baseline format.

## Visual table

Use a visual table for a quick, memorable impression of rank or relative amount.

- Follow “more is more”: larger quantities must produce greater extent, count, or appropriately ordered intensity—not less.
- Use pictures or symbols that depict the represented entity or have a familiar conventional meaning. Decorative imagery that competes with the encoding is not evidence.
- Compare extents at the same orientation and, when possible, from a common baseline.
- Prefer repeated identical symbols with a declared unit over proportionally scaling an icon in both height and width.
- Do not vary height and width together to encode a single amount: area perception distorts the comparison.
- Do not assign separate variables to integral dimensions such as the height and width of the same object. Use separable channels or aligned panels instead.
- Use partial symbols only when the fractional convention is obvious and accurate; otherwise choose a continuous length encoding.
- Keep symbol counts manageable. If counting becomes laborious, use bars, dots, or a conventional table.

## Rendering and review

- Verify that every visible share equals the validated input value and that displayed parts reconcile with the declared whole within the contract's stated tolerance.
- Inspect labels at final size, not only in the interactive plotting window.
- Check grayscale and color-vision robustness when color distinguishes categories.
- Confirm that emphasis does not alter perceived magnitude.
- Confirm that the evidence CSV alone contains the values needed to rebuild the graph or table manually in Excel; styling instructions are deliberately out of scope.


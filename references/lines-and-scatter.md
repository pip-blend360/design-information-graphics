# Lines and Scatter Plots

## Choose

Use lines for supplied observations over time or another meaningful ordered dimension. Use slope charts for a small number of endpoint comparisons and small multiples for many series. Use scatterplots for association between two quantitative variables; encode groups only when useful. Connect points only when sequence has meaning.

## Require

For lines, require order/time, series IDs, values, and explicit missing-observation semantics. For scatterplots, require paired x/y values at the declared observation grain, units, and identifiers. Accept only supplied interval bounds, fitted curves, or summary lines; do not fit models, bin observations, or calculate smoothing.

## Design and check

Sort visually without changing values; never bridge missing periods as if observed. Use distinguishable series and direct endpoint labels where feasible. Line/scatter axes need not start at zero, but range choices must not mislead. Label log scales explicitly and require valid positive values. Avoid causal claims from association. Use transparency for overplotting without altering records; do not jitter unless it is explicitly appropriate and disclosed. Verify mark counts, gaps, time spacing, paired values, and annotations.

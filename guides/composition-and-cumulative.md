# Stacked Composition and Cumulative Totals

## Choose

Use stacked bars for components contributing to totals across groups. Use layered/stacked area charts for supplied component values over ordered time when total and broad composition matter. Use a line or bar for an upstream running total. These are distinct relationships: a stack is not automatically a running total.

## Require

Require prepared component values, category/series IDs, units, meaningful ordering, and complete coverage of the declared total. Require running totals already calculated upstream. Verify uniqueness, coverage, missing values, and agreement with supplied totals using a declared tolerance. Do not cumulatively sum records analytically. Computing stack boundaries for drawing supplied components is a graphical-coordinate operation.

## Design and check

Keep layer order and colors stable; explain that interior layers lack a common baseline. Prefer grouped bars or small multiples when precise component comparison matters. Do not interpolate across missing periods or normalize to percentages without supplied shares. Mixed-sign stacks need explicit diverging treatment; otherwise choose another form. Check total height, component labels, chronological spacing, and whether stacking implies a false whole.

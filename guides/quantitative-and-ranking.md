# Quantitative Comparisons and Rank Order

## Choose

Use horizontal bars for long category names or ranking, vertical bars for short ordered categories, grouped bars for a few series, and small multiples for many series. Use dots for precise comparisons and intervals for supplied uncertainty. Use dumbbells or slope charts for two supplied endpoints; never infer change metrics.

## Require

Require one supplied value per displayed category/series at the declared grain, units, category meaning, and supplied uncertainty bounds if used. Verify uniqueness and numeric validity; do not aggregate duplicates or invent omitted categories.

## Design and check

Start bar-length axes at zero. Preserve meaningful natural order; otherwise rank visually by supplied values with explicit tie handling. Show signed values around a clear zero. Keep grouped and faceted scales comparable where comparison requires it. Dot plots may use a narrower range with clear ticks and disclosure. Avoid excessive groups, decorative area, clipped bars, and unsupported statistical summaries. Disable Seaborn aggregation and uncertainty estimation when plotting prepared values.

"""ds_charts - client-ready driver charts for two-segment "what goes with a bigger / more frequent outcome" models.

    from ds_charts import Units, effect_bars, marginal_curves, importance_bars, fit_bars, gap_bars, scorecard_table
    from ds_charts.synthetic import make_example_tables      # demo data with the expected columns

Every chart takes a plain DataFrame (column contract in each docstring and in README.md) and returns a Figure.
"""
from .style import PALETTE, Units, apply_style, save_fig, DEFAULT_FOOTNOTE
from .charts import (effect_bars, effect_bars_single, ranking_bars, marginal_curve, marginal_curves,
                     importance_bars, fit_bars, gap_bars, scorecard_table, scorecard_figure, segment_distributions)

__version__ = "1.0.0"

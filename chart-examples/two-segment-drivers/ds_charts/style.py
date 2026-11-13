"""Shared look for every ds_charts figure: palette, fonts, unit formatting, saving.

Palette: two segment colours (blue / orange) and a raise / lower pair (blue / red), validated for colour-vision
deficiency and contrast on a white surface (adjacent-pair CVD dE >= 21, all >= 3:1 contrast). Grey is reserved for
"held / not recommended" and for context features, so colour never has to carry meaning alone - every chart also
labels values directly.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass

import matplotlib.pyplot as plt

PALETTE = {
    "seg_1": "#2a78d6",      # first segment (e.g. Mid)
    "seg_2": "#eb6834",      # second segment (e.g. High / Best Customers)
    "up": "#2a78d6",         # behaviour goes with a HIGHER outcome
    "down": "#e34948",       # behaviour goes with a LOWER outcome
    "hold": "#bdbcb6",       # did not pass the recommendation gates
    "context": "#52514e",    # context / control feature (who the member is)
    "flag": "#d4d3cd",       # coverage / missing-value flag
    "ink": "#0b0b0b",        # primary text
    "ink_2": "#52514e",      # secondary text, footnotes
    "grid": "#e6e5e0",
    "axis": "#bdbcb6",
    "card": "#f3efe4",
    "surface": "#ffffff",
}
SEGMENT_COLORS = [PALETTE["seg_1"], PALETTE["seg_2"]]

DEFAULT_FOOTNOTE = "Associations from a model, not proven causes; a holdout test confirms lift."


def apply_style() -> None:
    """Set matplotlib defaults once per session (fonts, quiet axes, white background)."""
    plt.rcParams.update({
        "font.size": 10.5, "font.family": "DejaVu Sans",
        "axes.edgecolor": PALETTE["axis"], "axes.labelcolor": PALETTE["ink_2"],
        "xtick.color": PALETTE["ink_2"], "ytick.color": PALETTE["ink_2"],
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "axes.titlesize": 13, "axes.labelsize": 10.5,
        "figure.dpi": 110, "savefig.dpi": 160,
        "figure.facecolor": PALETTE["surface"], "savefig.facecolor": PALETTE["surface"],
        "axes.facecolor": PALETTE["surface"],
    })


@dataclass
class Units:
    """How values of the outcome are written: Units("$", "per order") or Units("orders", "per year")."""
    symbol: str = "$"
    per: str = ""
    dp: int = 2

    @property
    def is_money(self) -> bool:
        return self.symbol == "$"

    def fmt(self, v: float, dp: int | None = None) -> str:
        if v is None or v != v:
            return "-"
        dp = self.dp if dp is None else dp
        return f"${v:,.{dp}f}" if self.is_money else f"{v:,.{dp}f} {self.symbol}"

    def signed(self, v: float, dp: int | None = None) -> str:
        if v is None or v != v:
            return "-"
        return ("+" if v >= 0 else "−") + self.fmt(abs(v), dp)

    def axis_fmt(self, dp: int = 0) -> str:
        return "${x:,.%df}" % dp if self.is_money else "{x:,.%df}" % dp

    def axis_formatter(self, dp: int = 0):
        """Tick formatter that writes -$15 as "\u2212$15" (minus before the currency sign)."""
        from matplotlib.ticker import FuncFormatter
        def _f(v, _):
            body = f"{abs(v):,.{dp}f}"
            body = f"${body}" if self.is_money else body
            return ("\u2212" if v < -1e-12 else "") + body
        return FuncFormatter(_f)


def footnote(fig, text: str, y: float = -0.02, size: float = 8.5) -> None:
    """Small grey note under the figure (source, method, caveat)."""
    if text:
        fig.text(0.01, y, text, ha="left", va="top", fontsize=size, color=PALETTE["ink_2"], wrap=True)


def clean_axes(ax, keep: str = "none") -> None:
    """Remove chart junk. keep='x' / 'y' leaves that axis line; 'none' strips all four."""
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(keep in (side, "both") or (keep == "x" and side == "bottom")
                                    or (keep == "y" and side == "left"))


def slug(text: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]+", "_", str(text)).strip("_").lower()[:60] or "figure"


def save_fig(fig, name: str, out_dir: str | None = None, dpi: int = 160) -> str | None:
    """Save as PNG to out_dir (created if needed). Returns the path, or None when out_dir is None."""
    if not out_dir:
        return None
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{slug(name)}.png")
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=PALETTE["surface"])
    return path

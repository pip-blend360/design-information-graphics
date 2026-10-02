"""Export a finalized graph and its exact tabular evidence locally."""
from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Sequence

import pandas as pd


class GraphicOutputError(ValueError):
    """A graph and data pair cannot be exported safely."""


def publish_bundle(*, figure, data: pd.DataFrame,
                   evidence_columns: Sequence[str], output_dir: str | Path,
                   graphic_id: str, version: int = 1,
                   formats: Sequence[str] = ("png",), dpi: int = 200) -> dict[str, Path]:
    """Export after finalization (or explicit export request).

    Validate inputs before calling. Pass the same prepared values used to draw
    the graph, including supplied benchmark/annotation values. Code stays in
    the caller's notebook/package. Existing exports are never overwritten.
    """
    if not isinstance(graphic_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", graphic_id):
        raise GraphicOutputError("graphic_id must use lowercase letters, numbers, and single hyphens")
    if type(version) is not int or version < 1:
        raise GraphicOutputError("version must be a positive integer")
    columns = list(evidence_columns)
    if not columns or len(set(columns)) != len(columns) or not data.columns.is_unique:
        raise GraphicOutputError("Evidence must have nonempty, unique column names")
    missing = [c for c in columns if c not in data.columns]
    if missing:
        raise GraphicOutputError(f"Missing evidence columns: {missing}")
    formats = tuple(formats)
    if not formats or len(set(formats)) != len(formats) or any(f not in ("png", "svg") for f in formats):
        raise GraphicOutputError("formats must contain png and/or svg without duplicates")
    if type(dpi) is not int or dpi <= 0:
        raise GraphicOutputError("dpi must be a positive integer")
    destination = Path(output_dir)
    stem = graphic_id if version == 1 else f"{graphic_id}-v{version:02d}"
    paths = {f: destination / f"{stem}.{f}" for f in (*formats, "csv")}
    existing = [str(p) for p in paths.values() if p.exists()]
    if existing:
        raise FileExistsError("Refusing to overwrite: " + ", ".join(existing))
    destination.mkdir(parents=True, exist_ok=True)
    committed = []
    # Stage every artifact before publishing; roll back this call's new files
    # if saving fails. Exclusive creation also protects against concurrent edits.
    with tempfile.TemporaryDirectory(prefix=".graph-export-", dir=destination) as tmp:
        staged = {k: Path(tmp) / p.name for k, p in paths.items()}
        data.loc[:, columns].to_csv(staged["csv"], index=False, encoding="utf-8")
        for fmt in formats:
            figure.savefig(staged[fmt], format=fmt, dpi=dpi, bbox_inches="tight")
        try:
            for key, target in paths.items():
                with target.open("xb") as handle:
                    committed.append(target)
                    handle.write(staged[key].read_bytes())
        except BaseException:
            for target in committed:
                target.unlink(missing_ok=True)
            raise
    return paths

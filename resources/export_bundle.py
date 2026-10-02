"""Publish versioned information-graphic outputs and evidence metadata."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Sequence

import matplotlib.figure
import pandas as pd
import yaml


class GraphicOutputError(ValueError):
    """Raise when a graphic bundle cannot be published safely."""


def _assert_graphic_id(graphic_id: str) -> None:
    if (
        not graphic_id
        or graphic_id.strip("abcdefghijklmnopqrstuvwxyz0123456789-")
        or graphic_id.startswith("-")
        or graphic_id.endswith("-")
        or "--" in graphic_id
    ):
        raise GraphicOutputError(
            "graphic_id must use lowercase letters, numbers, and single hyphens."
        )


def publish_bundle(
    *,
    figure: matplotlib.figure.Figure,
    data: pd.DataFrame,
    evidence_columns: Sequence[str],
    output_dir: str | Path,
    graphic_id: str,
    version: int,
    title: str,
    source_dataframe: str,
    grain: Sequence[str],
    brand_profile: str | None = None,
    brand_profile_version: int | None = None,
    extra_metadata: Mapping[str, Any] | None = None,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Write PNG, SVG, minimum evidence CSV, and YAML metadata."""
    _assert_graphic_id(graphic_id)
    if version < 1:
        raise GraphicOutputError("version must be a positive integer")

    missing = sorted(set(evidence_columns).difference(data.columns))
    if missing:
        raise GraphicOutputError(
            f"Cannot publish evidence CSV; missing columns: {missing}."
        )

    destination = Path(output_dir)
    stem = graphic_id if version == 1 else f"{graphic_id}-v{version}"
    paths = {
        "png": destination / f"{stem}.png",
        "svg": destination / f"{stem}.svg",
        "csv": destination / f"{stem}.csv",
        "metadata": destination / f"{stem}.metadata.yaml",
    }
    existing = [str(path) for path in paths.values() if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "Refusing to overwrite existing graphic artifacts: " + ", ".join(existing)
        )

    destination.mkdir(parents=True, exist_ok=True)
    evidence = data.loc[:, list(evidence_columns)].copy()
    csv_bytes = evidence.to_csv(index=False).encode("utf-8")

    paths["csv"].write_bytes(csv_bytes)
    figure.savefig(paths["png"], dpi=200, bbox_inches="tight")
    figure.savefig(paths["svg"], bbox_inches="tight")

    metadata: dict[str, Any] = {
        "graphic_id": graphic_id,
        "version": version,
        "title": title,
        "source_dataframe": source_dataframe,
        "grain": list(grain),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": {key: path.name for key, path in paths.items() if key != "metadata"},
        "evidence": {
            "rows": len(evidence),
            "columns": list(evidence.columns),
            "sha256": sha256(csv_bytes).hexdigest(),
        },
    }
    if brand_profile:
        metadata["brand_profile"] = {
            "id": brand_profile,
            "version": brand_profile_version,
        }
    if extra_metadata:
        metadata.update(dict(extra_metadata))

    paths["metadata"].write_text(
        yaml.safe_dump(metadata, sort_keys=False), encoding="utf-8"
    )
    return paths

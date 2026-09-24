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
    data: pd.DataFrame | None = None,
    evidence_columns: Sequence[str] | None = None,
    evidence_tables: Mapping[str, tuple[pd.DataFrame, Sequence[str]]] | None = None,
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
    """Write PNG, SVG, Excel-ready evidence CSV file(s), and YAML metadata.

    Use ``data`` with ``evidence_columns`` for one evidence table. Use
    ``evidence_tables`` for panels with different validated grains; its keys
    become lowercase-hyphenated CSV suffixes. These routes are mutually
    exclusive.
    """
    _assert_graphic_id(graphic_id)
    if version < 1:
        raise GraphicOutputError("version must be a positive integer")

    using_single = data is not None or evidence_columns is not None
    using_multiple = evidence_tables is not None
    if using_single == using_multiple:
        raise GraphicOutputError(
            "Provide either data with evidence_columns, or evidence_tables."
        )

    tables: dict[str | None, tuple[pd.DataFrame, Sequence[str]]]
    if using_multiple:
        if not evidence_tables:
            raise GraphicOutputError("evidence_tables must not be empty.")
        tables = {}
        for table_id, table_spec in evidence_tables.items():
            _assert_graphic_id(table_id)
            tables[table_id] = table_spec
    else:
        if data is None or evidence_columns is None:
            raise GraphicOutputError(
                "Single-table publishing requires data and evidence_columns."
            )
        tables = {None: (data, evidence_columns)}

    evidence_frames: dict[str | None, pd.DataFrame] = {}
    csv_bytes_by_id: dict[str | None, bytes] = {}
    for table_id, (table_data, columns) in tables.items():
        if not isinstance(table_data, pd.DataFrame):
            raise GraphicOutputError(
                f"Evidence table {table_id or 'default'!r} must be a DataFrame."
            )
        missing = sorted(set(columns).difference(table_data.columns))
        if missing:
            raise GraphicOutputError(
                f"Cannot publish evidence CSV {table_id or 'default'!r}; "
                f"missing columns: {missing}."
            )
        evidence = table_data.loc[:, list(columns)].copy()
        evidence_frames[table_id] = evidence
        csv_bytes_by_id[table_id] = evidence.to_csv(index=False).encode("utf-8")

    destination = Path(output_dir)
    stem = graphic_id if version == 1 else f"{graphic_id}-v{version}"
    paths: dict[str, Path] = {
        "png": destination / f"{stem}.png",
        "svg": destination / f"{stem}.svg",
        "metadata": destination / f"{stem}.metadata.yaml",
    }
    for table_id in tables:
        key = "csv" if table_id is None else f"csv_{table_id.replace('-', '_')}"
        suffix = "" if table_id is None else f"-{table_id}"
        paths[key] = destination / f"{stem}{suffix}.csv"
    existing = [str(path) for path in paths.values() if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "Refusing to overwrite existing graphic artifacts: " + ", ".join(existing)
        )

    destination.mkdir(parents=True, exist_ok=True)
    for table_id, csv_bytes in csv_bytes_by_id.items():
        key = "csv" if table_id is None else f"csv_{table_id.replace('-', '_')}"
        paths[key].write_bytes(csv_bytes)
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
    }
    evidence_metadata = {
        (table_id or "default"): {
            "file": paths[
                "csv" if table_id is None else f"csv_{table_id.replace('-', '_')}"
            ].name,
            "rows": len(evidence_frames[table_id]),
            "columns": list(evidence_frames[table_id].columns),
            "sha256": sha256(csv_bytes_by_id[table_id]).hexdigest(),
        }
        for table_id in tables
    }
    metadata["evidence"] = (
        evidence_metadata["default"] if set(evidence_metadata) == {"default"}
        else evidence_metadata
    )
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

"""Read-only validation utilities for information-graphic inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import pandas as pd
from pandas.api import types as ptypes


class VisualizationDataError(ValueError):
    """Raise when a DataFrame violates a visualization contract."""


@dataclass(frozen=True)
class FieldContract:
    name: str
    semantic_type: str = "any"
    nullable: bool = False
    unit: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    allowed_values: tuple[Any, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DataContract:
    grain: tuple[str, ...]
    fields: tuple[FieldContract, ...]
    description: str = ""


def _type_matches(series: pd.Series, semantic_type: str) -> bool:
    checks = {
        "any": lambda s: True,
        "numeric": ptypes.is_numeric_dtype,
        "integer": ptypes.is_integer_dtype,
        "boolean": ptypes.is_bool_dtype,
        "datetime": ptypes.is_datetime64_any_dtype,
        "category": lambda s: (
            ptypes.is_object_dtype(s.dtype)
            or isinstance(s.dtype, pd.CategoricalDtype)
            or ptypes.is_string_dtype(s.dtype)
        ),
        "string": lambda s: (
            ptypes.is_string_dtype(s.dtype) or ptypes.is_object_dtype(s.dtype)
        ),
    }
    if semantic_type not in checks:
        raise ValueError(f"Unsupported semantic type: {semantic_type!r}")
    return bool(checks[semantic_type](series))


def _fail(rule: str, expected: str, observed: str, correction: str) -> None:
    raise VisualizationDataError(
        "Visualization input validation failed.\n\n"
        f"Rule: {rule}\nExpected: {expected}\nObserved: {observed}\n\n"
        "Why this blocks rendering:\n"
        "Rendering incompatible data could misstate the evidence.\n\n"
        f"Required correction:\n{correction}"
    )


def validate_dataframe(data: pd.DataFrame, contract: DataContract) -> None:
    """Validate data without modifying it; return None on success."""
    if not isinstance(data, pd.DataFrame):
        _fail(
            "input object",
            "an in-memory pandas DataFrame",
            type(data).__name__,
            "Provide the analysis-ready result as a pandas DataFrame.",
        )

    required = [item.name for item in contract.fields]
    missing = sorted(set(required).difference(data.columns))
    if missing:
        _fail(
            "required columns",
            f"columns {required}",
            f"missing {missing}",
            "Create the missing fields in the upstream data-preparation workflow.",
        )

    missing_grain = sorted(set(contract.grain).difference(data.columns))
    if missing_grain:
        _fail(
            "declared grain",
            f"grain columns {list(contract.grain)}",
            f"missing {missing_grain}",
            "Provide the declared grain columns upstream.",
        )

    if contract.grain and data.duplicated(list(contract.grain), keep=False).any():
        duplicate = data.duplicated(list(contract.grain), keep=False)
        examples = (
            data.loc[duplicate, list(contract.grain)]
            .drop_duplicates()
            .head(5)
            .to_dict(orient="records")
        )
        _fail(
            "unique grain",
            f"one row per {list(contract.grain)}",
            f"duplicate grain values; examples: {examples}",
            "Resolve duplicates upstream. This skill will not aggregate or deduplicate them.",
        )

    for spec in contract.fields:
        series = data[spec.name]
        if not _type_matches(series, spec.semantic_type):
            _fail(
                f"field {spec.name!r} type",
                spec.semantic_type,
                str(series.dtype),
                "Provide the declared type upstream; do not rely on implicit coercion.",
            )

        null_count = int(series.isna().sum())
        if not spec.nullable and null_count:
            _fail(
                f"field {spec.name!r} null policy",
                "no missing values",
                f"{null_count} missing values",
                "Resolve or explicitly redefine missing values upstream.",
            )

        observed = series.dropna()
        if spec.minimum is not None and not observed.empty and (observed < spec.minimum).any():
            _fail(
                f"field {spec.name!r} lower bound",
                f"values >= {spec.minimum}",
                f"minimum {observed.min()!r}",
                "Correct the values or declared unit upstream.",
            )
        if spec.maximum is not None and not observed.empty and (observed > spec.maximum).any():
            _fail(
                f"field {spec.name!r} upper bound",
                f"values <= {spec.maximum}",
                f"maximum {observed.max()!r}",
                "Correct the values or declared unit upstream.",
            )
        if spec.allowed_values:
            unexpected = sorted(
                set(observed.unique()).difference(spec.allowed_values), key=str
            )
            if unexpected:
                _fail(
                    f"field {spec.name!r} categories",
                    f"values in {list(spec.allowed_values)}",
                    f"unexpected values {unexpected[:10]}",
                    "Resolve or explicitly approve category definitions upstream.",
                )


def contract_from_mapping(raw: Mapping[str, Any]) -> DataContract:
    """Build a contract from a plain mapping such as parsed YAML."""
    fields = tuple(
        FieldContract(
            name=name,
            semantic_type=spec.get("semantic_type", "any"),
            nullable=bool(spec.get("nullable", False)),
            unit=spec.get("unit"),
            minimum=spec.get("minimum"),
            maximum=spec.get("maximum"),
            allowed_values=tuple(spec.get("allowed_values", ())),
        )
        for name, spec in raw.get("fields", {}).items()
    )
    return DataContract(
        grain=tuple(raw.get("unique_by", ())),
        fields=fields,
        description=raw.get("grain", ""),
    )

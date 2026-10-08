"""Reusable data-cleaning steps for tabular files."""

from __future__ import annotations

import re
from typing import Any

import pandas as pd


def normalize_column_name(name: Any) -> str:
    """Convert a column label to lowercase snake_case."""
    text = re.sub(r"[^0-9a-zA-Z]+", "_", str(name).strip().lower())
    return re.sub(r"_+", "_", text).strip("_") or "unnamed_column"


def clean_dataframe(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Clean a dataframe and return it alongside a concise audit summary."""
    if raw.empty and len(raw.columns) == 0:
        raise ValueError("The input file has no columns. Check that the first row contains headers.")

    original_rows = len(raw)
    original_columns = [str(column) for column in raw.columns]
    frame = raw.copy()
    frame.columns = [normalize_column_name(column) for column in frame.columns]

    # Make repeated headers unique after normalization (e.g. "Email" and "email").
    seen: dict[str, int] = {}
    unique_columns = []
    for column in frame.columns:
        seen[column] = seen.get(column, 0) + 1
        unique_columns.append(column if seen[column] == 1 else f"{column}_{seen[column]}")
    frame.columns = unique_columns

    for column in frame.select_dtypes(include=["object", "string"]).columns:
        frame[column] = frame[column].map(lambda value: value.strip() if isinstance(value, str) else value)
        frame[column] = frame[column].replace("", pd.NA)

    missing_before = int(frame.isna().sum().sum())
    duplicate_rows = int(frame.duplicated().sum())
    frame = frame.drop_duplicates().copy()

    fill_rules: dict[str, str] = {}
    for column in frame.columns:
        if not frame[column].isna().any():
            fill_rules[column] = "No missing values"
        elif pd.api.types.is_numeric_dtype(frame[column]):
            median = frame[column].median()
            fill_value = 0 if pd.isna(median) else median
            frame[column] = frame[column].fillna(fill_value)
            fill_rules[column] = f"Median ({fill_value:g})" if isinstance(fill_value, (int, float)) else "Median"
        else:
            frame[column] = frame[column].fillna("Unknown")
            fill_rules[column] = "Unknown"

    summary: dict[str, Any] = {
        "rows_before": original_rows,
        "rows_after": len(frame),
        "duplicates_removed": duplicate_rows,
        "missing_cells_before_fill": missing_before,
        "missing_cells_after_fill": int(frame.isna().sum().sum()),
        "columns_before": len(original_columns),
        "columns_after": len(frame.columns),
        "original_columns": original_columns,
        "cleaned_columns": list(frame.columns),
        "fill_rules": fill_rules,
    }
    return frame, summary

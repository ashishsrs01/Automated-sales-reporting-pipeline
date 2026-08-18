from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = frozenset(
    {
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product",
        "Category",
        "Region",
        "Salesperson",
        "Quantity",
        "Unit_Price",
    }
)


@dataclass(frozen=True)
class SchemaValidationResult:
    """Result of validating a DataFrame schema."""

    is_valid: bool
    missing_columns: tuple[str, ...]
    unexpected_columns: tuple[str, ...]
    duplicate_columns: tuple[str, ...]


def find_duplicate_columns(columns: pd.Index) -> tuple[str, ...]:
    """Return duplicate column names."""
    duplicates = columns[columns.duplicated()].unique()
    return tuple(sorted(str(column) for column in duplicates))


def validate_schema(dataframe: pd.DataFrame) -> SchemaValidationResult:
    """Validate the structure of an incoming sales DataFrame."""
    columns = dataframe.columns

    missing_columns = tuple(sorted(REQUIRED_COLUMNS - set(columns)))
    unexpected_columns = tuple(sorted(set(columns) - REQUIRED_COLUMNS))
    duplicate_columns = find_duplicate_columns(columns)

    is_valid = not (
        bool(missing_columns)
        or bool(unexpected_columns)
        or bool(duplicate_columns)
    )

    return SchemaValidationResult(
        is_valid=is_valid,
        missing_columns=missing_columns,
        unexpected_columns=unexpected_columns,
        duplicate_columns=duplicate_columns,
    )

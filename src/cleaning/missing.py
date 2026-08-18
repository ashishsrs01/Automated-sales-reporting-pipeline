from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CleaningStats:
    """Statistics produced while handling invalid records."""

    rows_before: int
    rows_after: int
    rows_removed: int
    missing_values_filled: int


REQUIRED_COLUMNS = (
    "Order_ID",
    "Order_Date",
    "Product",
    "Quantity",
    "Unit_Price",
)


def fill_allowed_missing_values(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:
    """Fill missing values only where policy permits."""
    cleaned = dataframe.copy()
    filled_count = 0

    fill_columns = (
        "Customer_ID",
        "Region",
        "Salesperson",
    )

    for column in fill_columns:
        if column not in cleaned.columns:
            continue

        missing = cleaned[column].isna()
        filled_count += int(missing.sum())

        cleaned.loc[missing, column] = "Unknown"

    return cleaned, filled_count


def remove_invalid_required_records(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:
    """Remove rows that cannot be safely repaired."""
    cleaned = dataframe.copy()

    required_mask = pd.Series(
        True,
        index=cleaned.index,
    )

    for column in REQUIRED_COLUMNS:
        if column not in cleaned.columns:
            continue

        required_mask &= cleaned[column].notna()

    if "Quantity" in cleaned.columns:
        required_mask &= cleaned["Quantity"] > 0

    if "Unit_Price" in cleaned.columns:
        required_mask &= cleaned["Unit_Price"] > 0

    rows_before = len(cleaned)

    cleaned = cleaned.loc[required_mask].copy()

    rows_removed = rows_before - len(cleaned)

    return cleaned, rows_removed


def handle_missing_and_invalid_records(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, CleaningStats]:
    """Apply the missing-value and invalid-record policy."""
    rows_before = len(dataframe)

    cleaned, missing_values_filled = (
        fill_allowed_missing_values(dataframe)
    )

    cleaned, rows_removed = remove_invalid_required_records(
        cleaned
    )

    stats = CleaningStats(
        rows_before=rows_before,
        rows_after=len(cleaned),
        rows_removed=rows_removed,
        missing_values_filled=missing_values_filled,
    )

    return cleaned, stats
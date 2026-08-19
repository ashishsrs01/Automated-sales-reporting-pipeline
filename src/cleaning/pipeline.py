from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .dates import normalize_order_date
from .duplicates import remove_duplicate_orders
from .missing import handle_missing_and_invalid_records
from .numeric import normalize_numeric_columns
from .text import normalize_text_columns


@dataclass(frozen=True)
class CleaningResult:
    """Result produced by the complete cleaning pipeline."""

    dataframe: pd.DataFrame
    rows_before: int
    rows_after: int
    rows_removed: int
    missing_values_filled: int
    duplicates_removed: int


def clean_dataset(
    dataframe: pd.DataFrame,
) -> CleaningResult:
    """Run the complete dataset cleaning pipeline."""
    rows_before = len(dataframe)

    cleaned = normalize_text_columns(dataframe)

    cleaned = normalize_order_date(cleaned)

    cleaned = normalize_numeric_columns(cleaned)

    cleaned, missing_stats = handle_missing_and_invalid_records(
        cleaned
    )

    cleaned, duplicates_removed = remove_duplicate_orders(
        cleaned
    )

    rows_removed = rows_before - len(cleaned)

    return CleaningResult(
        dataframe=cleaned,
        rows_before=rows_before,
        rows_after=len(cleaned),
        rows_removed=rows_removed,
        missing_values_filled=missing_stats.missing_values_filled,
        duplicates_removed=duplicates_removed,
    )
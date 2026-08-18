from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class CorruptionStats:
    duplicate_rows: int = 0
    missing_values: int = 0
    text_errors: int = 0
    date_errors: int = 0
    invalid_quantities: int = 0
    invalid_prices: int = 0


def inject_duplicates(
    dataframe: pd.DataFrame,
    rng: np.random.Generator,
    rate: float = 0.015,
) -> tuple[pd.DataFrame, int]:
    """Duplicate a percentage of existing rows."""
    count = int(len(dataframe) * rate)

    if count == 0:
        return dataframe, 0

    duplicate_rows = dataframe.sample(
        n=count,
        random_state=int(rng.integers(0, 1_000_000)),
    )

    result = pd.concat(
        [dataframe, duplicate_rows],
        ignore_index=True,
    )

    return result, count


def inject_missing_values(
    dataframe: pd.DataFrame,
    rng: np.random.Generator,
    rate: float = 0.02,
) -> tuple[pd.DataFrame, int]:
    """Inject missing values into selected business columns."""
    result = dataframe.copy()

    columns = (
        "Customer_ID",
        "Salesperson",
        "Region",
    )

    total_changes = 0

    for column in columns:
        count = int(len(result) * rate)

        indexes = rng.choice(
            result.index,
            size=count,
            replace=False,
        )

        result.loc[indexes, column] = pd.NA
        total_changes += count

    return result, total_changes


def inject_text_errors(
    dataframe: pd.DataFrame,
    rng: np.random.Generator,
    rate: float = 0.02,
) -> tuple[pd.DataFrame, int]:
    """Inject capitalization and whitespace inconsistencies."""
    result = dataframe.copy()

    columns = ("Category", "Region")

    total_changes = 0

    for column in columns:
        count = int(len(result) * rate)

        indexes = rng.choice(
            result.index,
            size=count,
            replace=False,
        )

        for index in indexes:
            value = result.at[index, column]

            if pd.isna(value):
                continue

            mode = rng.integers(0, 3)

            if mode == 0:
                result.at[index, column] = str(value).lower()
            elif mode == 1:
                result.at[index, column] = f" {value}"
            else:
                result.at[index, column] = f"{value} "

            total_changes += 1

    return result, total_changes


def inject_date_errors(
    dataframe: pd.DataFrame,
    rng: np.random.Generator,
    rate: float = 0.01,
) -> tuple[pd.DataFrame, int]:
    """Inject invalid date values."""
    result = dataframe.copy()

    count = int(len(result) * rate)

    if count == 0:
        return result, 0

    if "Order_Date" not in result.columns:
        return result, 0

    indexes = rng.choice(
        result.index,
        size=count,
        replace=False,
    )

    result.loc[indexes, "Order_Date"] = pd.NaT

    return result, count


def inject_invalid_numbers(
    dataframe: pd.DataFrame,
    rng: np.random.Generator,
    rate: float = 0.005,
) -> tuple[pd.DataFrame, int, int]:
    """Inject invalid quantity and price values."""
    result = dataframe.copy()

    count = int(len(result) * rate)

    quantity_indexes = rng.choice(
        result.index,
        size=count,
        replace=False,
    )

    price_indexes = rng.choice(
        result.index,
        size=count,
        replace=False,
    )

    result.loc[quantity_indexes, "Quantity"] = -1
    result.loc[price_indexes, "Unit_Price"] = -100

    return result, count, count


def corrupt_dataset(
    dataframe: pd.DataFrame,
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, CorruptionStats]:
    """Apply all controlled data-quality corruptions."""
    stats = CorruptionStats()

    result, stats.duplicate_rows = inject_duplicates(
        dataframe,
        rng,
    )

    result, stats.missing_values = inject_missing_values(
        result,
        rng,
    )

    result, stats.text_errors = inject_text_errors(
        result,
        rng,
    )

    result, stats.date_errors = inject_date_errors(
        result,
        rng,
    )

    (
        result,
        stats.invalid_quantities,
        stats.invalid_prices,
    ) = inject_invalid_numbers(
        result,
        rng,
    )

    return result, stats
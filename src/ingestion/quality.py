from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

VALID_REGIONS = frozenset(
    {
        "North",
        "South",
        "East",
        "West",
        "Central",
    }
)

ORDER_ID_PATTERN = r"^ORD-\d{6}-\d{5}$"


@dataclass(frozen=True)
class DataQualityResult:
    """Result of data-level quality validation."""

    missing_values: dict[str, int]
    invalid_order_ids: int
    invalid_dates: int
    invalid_regions: int
    invalid_quantities: int
    invalid_prices: int

    @property
    def is_valid(self) -> bool:
        """Return whether the dataset passes all quality checks."""
        return not any(
            (
                self.invalid_order_ids,
                self.invalid_dates,
                self.invalid_regions,
                self.invalid_quantities,
                self.invalid_prices,
                sum(self.missing_values.values()),
            )
        )
    

def find_missing_values(
    dataframe: pd.DataFrame,
) -> dict[str, int]:
    """Return missing-value counts for columns containing missing data."""
    missing = dataframe.isna().sum()

    return {
        column: int(count)
        for column, count in missing.items()
        if count > 0
    }


def count_invalid_order_ids(
    dataframe: pd.DataFrame,
) -> int:
    """Count malformed order identifiers."""
    valid = dataframe["Order_ID"].astype("string").str.match(
        ORDER_ID_PATTERN,
        na=False,
    )

    return int((~valid).sum())

def count_invalid_dates(
    dataframe: pd.DataFrame,
) -> int:
    """Count values that cannot be interpreted as dates."""
    parsed = pd.to_datetime(
        dataframe["Order_Date"],
        errors="coerce",
        format="mixed",
    )

    return int(parsed.isna().sum())


def count_invalid_regions(
    dataframe: pd.DataFrame,
) -> int:
    """Count unexpected region values."""
    valid = dataframe["Region"].isin(VALID_REGIONS)

    return int((~valid).sum())


def count_invalid_quantities(
    dataframe: pd.DataFrame,
) -> int:
    """Count non-positive or non-numeric quantities."""
    numeric = pd.to_numeric(
        dataframe["Quantity"],
        errors="coerce",
    )

    invalid = numeric.isna() | (numeric <= 0)

    return int(invalid.sum())


def count_invalid_prices(
    dataframe: pd.DataFrame,
) -> int:
    """Count non-positive or non-numeric prices."""
    numeric = pd.to_numeric(
        dataframe["Unit_Price"],
        errors="coerce",
    )

    invalid = numeric.isna() | (numeric <= 0)

    return int(invalid.sum())


def validate_data_quality(
    dataframe: pd.DataFrame,
) -> DataQualityResult:
    """Run all data-level quality checks."""
    return DataQualityResult(
        missing_values=find_missing_values(dataframe),
        invalid_order_ids=count_invalid_order_ids(dataframe),
        invalid_dates=count_invalid_dates(dataframe),
        invalid_regions=count_invalid_regions(dataframe),
        invalid_quantities=count_invalid_quantities(dataframe),
        invalid_prices=count_invalid_prices(dataframe),
    )
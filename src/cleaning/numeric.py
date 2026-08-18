from __future__ import annotations

import pandas as pd


def normalize_quantity(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Convert Quantity to numeric values."""
    cleaned = dataframe.copy()

    if "Quantity" in cleaned.columns:
        cleaned["Quantity"] = pd.to_numeric(
            cleaned["Quantity"],
            errors="coerce",
        )

    return cleaned


def normalize_unit_price(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Convert Unit_Price to numeric values."""
    cleaned = dataframe.copy()

    if "Unit_Price" in cleaned.columns:
        cleaned["Unit_Price"] = pd.to_numeric(
            cleaned["Unit_Price"],
            errors="coerce",
        )

    return cleaned


def normalize_numeric_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Normalize supported numeric fields."""
    cleaned = dataframe.copy()

    cleaned = normalize_quantity(cleaned)
    cleaned = normalize_unit_price(cleaned)

    return cleaned
from __future__ import annotations

import pandas as pd

REGION_MAP = {
    "north": "North",
    "south": "South",
    "east": "East",
    "west": "West",
    "central": "Central",
}

CATEGORY_MAP = {
    "electronics": "Electronics",
    "furniture": "Furniture",
    "office supplies": "Office Supplies",
    "accessories": "Accessories",
}


def normalize_text(value: object) -> object:
    """Strip surrounding whitespace from a value."""
    if pd.isna(value):
        return value

    return str(value).strip()


def normalize_region(value: object) -> object:
    """Normalize a region to its canonical representation."""
    value = normalize_text(value)

    if pd.isna(value):
        return value

    return REGION_MAP.get(str(value).lower(), "Unknown")


def normalize_category(value: object) -> object:
    """Normalize a category to its canonical representation."""
    value = normalize_text(value)

    if pd.isna(value):
        return value

    return CATEGORY_MAP.get(
        str(value).lower(),
        "Unknown",
    )


def normalize_text_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Return a copy with supported text fields standardized."""
    cleaned = dataframe.copy()

    for column in ("Product", "Salesperson", "Customer_ID"):
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].map(
                normalize_text
            )

    if "Region" in cleaned.columns:
        cleaned["Region"] = cleaned["Region"].map(
            normalize_region
        )

    if "Category" in cleaned.columns:
        cleaned["Category"] = cleaned["Category"].map(
            normalize_category
        )

    return cleaned
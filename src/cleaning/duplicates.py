from __future__ import annotations

import pandas as pd


def remove_duplicate_orders(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:
    """Remove duplicate orders while keeping the first occurrence."""
    cleaned = dataframe.copy()

    if "Order_ID" not in cleaned.columns:
        return cleaned, 0

    duplicate_mask = cleaned.duplicated(
        subset=["Order_ID"],
        keep="first",
    )

    duplicates_removed = int(duplicate_mask.sum())

    cleaned = cleaned.loc[~duplicate_mask].copy()

    return cleaned, duplicates_removed
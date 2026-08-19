from __future__ import annotations

import pandas as pd


def calculate_revenue(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate transaction-level revenue."""
    required_columns = {
        "Quantity",
        "Unit_Price",
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            "Missing required columns for revenue calculation: "
            f"{sorted(missing_columns)}"
        )

    result = dataframe.copy()

    result["Revenue"] = (
        result["Quantity"] * result["Unit_Price"]
    )

    return result

def classify_order_size(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Classify orders based on transaction revenue."""
    if "Revenue" not in dataframe.columns:
        raise ValueError(
            "Revenue must be calculated before "
            "classifying order size."
        )

    result = dataframe.copy()

    result["Order_Size"] = pd.cut(
        result["Revenue"],
        bins=[-float("inf"), 500, 2000, float("inf")],
        labels=["Small", "Medium", "Large"],
        right=False,
    )

    return result
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class BusinessInsights:
    """Deterministic insights derived from business metrics."""

    top_region: str | None
    top_category: str | None
    top_product: str | None
    top_salesperson: str | None

    best_month: str | None
    worst_month: str | None

    strongest_growth_month: str | None
    strongest_growth_rate: float | None

    largest_decline_month: str | None
    largest_decline_rate: float | None

def _top_dimension(
    dataframe: pd.DataFrame,
    dimension: str,
) -> str | None:
    """Return the highest-revenue value for a dimension."""
    if dataframe.empty:
        return None

    if dimension not in dataframe.columns:
        raise ValueError(
            f"Missing required column: {dimension}"
        )

    if "Revenue" not in dataframe.columns:
        raise ValueError(
            "Missing required column: Revenue"
        )

    grouped = (
        dataframe.groupby(dimension, dropna=False)["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    if grouped.empty:
        return None

    return str(grouped.index[0])

def top_region(
    dataframe: pd.DataFrame,
) -> str | None:
    """Return the highest-revenue region."""
    return _top_dimension(dataframe, "Region")


def top_category(
    dataframe: pd.DataFrame,
) -> str | None:
    """Return the highest-revenue category."""
    return _top_dimension(dataframe, "Category")


def top_product(
    dataframe: pd.DataFrame,
) -> str | None:
    """Return the highest-revenue product."""
    return _top_dimension(dataframe, "Product")


def top_salesperson(
    dataframe: pd.DataFrame,
) -> str | None:
    """Return the highest-revenue salesperson."""
    return _top_dimension(dataframe, "Salesperson")


def best_revenue_month(
    monthly_dataframe: pd.DataFrame,
) -> str | None:
    """Return the month with the highest revenue."""
    if monthly_dataframe.empty:
        return None

    required = {"Month", "Revenue"}

    missing = required - set(monthly_dataframe.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    index = monthly_dataframe["Revenue"].idxmax()

    return str(monthly_dataframe.loc[index, "Month"])


def worst_revenue_month(
    monthly_dataframe: pd.DataFrame,
) -> str | None:
    """Return the month with the lowest revenue."""
    if monthly_dataframe.empty:
        return None

    required = {"Month", "Revenue"}

    missing = required - set(monthly_dataframe.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    index = monthly_dataframe["Revenue"].idxmin()

    return str(monthly_dataframe.loc[index, "Month"])


def strongest_growth(
    monthly_dataframe: pd.DataFrame,
) -> tuple[str | None, float | None]:
    """Return the month with the strongest positive growth."""
    required = {"Month", "MoM_Growth"}

    missing = required - set(monthly_dataframe.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    valid = monthly_dataframe.dropna(
        subset=["MoM_Growth"]
    )

    positive = valid[
        valid["MoM_Growth"] > 0
    ]

    if positive.empty:
        return None, None

    index = positive["MoM_Growth"].idxmax()

    return (
        str(positive.loc[index, "Month"]),
        float(positive.loc[index, "MoM_Growth"]),
    )

def largest_decline(
    monthly_dataframe: pd.DataFrame,
) -> tuple[str | None, float | None]:
    """Return the month with the largest revenue decline."""
    required = {"Month", "MoM_Growth"}

    missing = required - set(monthly_dataframe.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    valid = monthly_dataframe.dropna(
        subset=["MoM_Growth"]
    )

    negative = valid[
        valid["MoM_Growth"] < 0
    ]

    if negative.empty:
        return None, None

    index = negative["MoM_Growth"].idxmin()

    return (
        str(negative.loc[index, "Month"]),
        float(negative.loc[index, "MoM_Growth"]),
    )


def generate_business_insights(
    dataframe: pd.DataFrame,
    monthly_dataframe: pd.DataFrame,
) -> BusinessInsights:
    """Generate deterministic business insights."""

    growth_month, growth_rate = strongest_growth(
        monthly_dataframe
    )

    decline_month, decline_rate = largest_decline(
        monthly_dataframe
    )

    return BusinessInsights(
        top_region=top_region(dataframe),
        top_category=top_category(dataframe),
        top_product=top_product(dataframe),
        top_salesperson=top_salesperson(dataframe),
        best_month=best_revenue_month(
            monthly_dataframe
        ),
        worst_month=worst_revenue_month(
            monthly_dataframe
        ),
        strongest_growth_month=growth_month,
        strongest_growth_rate=growth_rate,
        largest_decline_month=decline_month,
        largest_decline_rate=decline_rate,
    )
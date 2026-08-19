import pandas as pd
import pytest

from src.analytics.insights import (
    generate_business_insights,
    largest_decline,
    strongest_growth,
    top_category,
    top_product,
    top_region,
    top_salesperson,
)


@pytest.fixture
def transaction_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Region": [
                "North",
                "South",
                "North",
                "West",
            ],
            "Category": [
                "Electronics",
                "Furniture",
                "Electronics",
                "Furniture",
            ],
            "Product": [
                "Laptop",
                "Desk",
                "Laptop",
                "Chair",
            ],
            "Salesperson": [
                "Alice",
                "Bob",
                "Alice",
                "Charlie",
            ],
            "Revenue": [
                1000.0,
                500.0,
                1500.0,
                300.0,
            ],
        }
    )


@pytest.fixture
def monthly_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Month": pd.period_range(
                "2026-01",
                periods=4,
                freq="M",
            ),
            "Revenue": [
                1000.0,
                1200.0,
                900.0,
                1500.0,
            ],
            "MoM_Growth": [
                None,
                20.0,
                -25.0,
                66.6667,
            ],
        }
    )

def test_top_region(
    transaction_data: pd.DataFrame,
) -> None:
    assert top_region(transaction_data) == "North"


def test_top_category(
    transaction_data: pd.DataFrame,
) -> None:
    assert top_category(transaction_data) == "Electronics"


def test_top_product(
    transaction_data: pd.DataFrame,
) -> None:
    assert top_product(transaction_data) == "Laptop"


def test_top_salesperson(
    transaction_data: pd.DataFrame,
) -> None:
    assert top_salesperson(transaction_data) == "Alice"


def test_strongest_growth(
    monthly_data: pd.DataFrame,
) -> None:
    month, rate = strongest_growth(monthly_data)

    assert month == "2026-04"
    assert rate == pytest.approx(66.6667)


def test_largest_decline(
    monthly_data: pd.DataFrame,
) -> None:
    month, rate = largest_decline(monthly_data)

    assert month == "2026-03"
    assert rate == pytest.approx(-25.0)

def test_generate_business_insights(
    transaction_data: pd.DataFrame,
    monthly_data: pd.DataFrame,
) -> None:
    result = generate_business_insights(
        transaction_data,
        monthly_data,
    )

    assert result.top_region == "North"
    assert result.top_category == "Electronics"
    assert result.top_product == "Laptop"
    assert result.top_salesperson == "Alice"

    assert result.best_month == "2026-04"
    assert result.worst_month == "2026-03"

    assert result.strongest_growth_month == "2026-04"
    assert result.largest_decline_month == "2026-03"
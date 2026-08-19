import pandas as pd

from src.analytics.pipeline import (
    AnalyticsResult,
    run_analytics,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Order_ID": [
                "ORD-001",
                "ORD-002",
                "ORD-003",
                "ORD-004",
            ],
            "Order_Date": pd.to_datetime(
                [
                    "2026-01-10",
                    "2026-01-20",
                    "2026-02-10",
                    "2026-02-20",
                ]
            ),
            "Customer_ID": [
                "CUST-001",
                "CUST-002",
                "CUST-003",
                "CUST-004",
            ],
            "Product": [
                "Laptop",
                "Mouse",
                "Laptop",
                "Keyboard",
            ],
            "Category": [
                "Electronics",
                "Electronics",
                "Electronics",
                "Electronics",
            ],
            "Region": [
                "North",
                "South",
                "North",
                "West",
            ],
            "Salesperson": [
                "Alice",
                "Bob",
                "Alice",
                "Charlie",
            ],
            "Quantity": [
                2,
                5,
                3,
                4,
            ],
            "Unit_Price": [
                1000.0,
                100.0,
                1000.0,
                200.0,
            ],
        }
    )


def test_run_analytics_returns_complete_result() -> None:
    result = run_analytics(sample_dataframe())

    assert isinstance(result, AnalyticsResult)

    assert result.overall_metrics["total_revenue"] == (2000.0 + 500.0 + 3000.0 + 800.0)

    assert result.overall_metrics["total_orders"] == 4

    assert result.overall_metrics["total_units"] == 14

    assert "Revenue" in result.enriched_data.columns

    assert "Order_Size" in result.enriched_data.columns

    assert not result.by_region.empty

    assert not result.by_category.empty

    assert not result.by_product.empty

    assert not result.by_salesperson.empty

    assert not result.monthly_metrics.empty


def test_monthly_metrics_include_growth() -> None:
    result = run_analytics(sample_dataframe())

    assert "MoM_Growth" in (result.monthly_metrics.columns)


def test_business_insights_are_generated() -> None:
    result = run_analytics(sample_dataframe())

    insights = result.business_insights

    assert insights.top_region == "North"

    assert insights.top_product == "Laptop"

    assert insights.top_salesperson == "Alice"

    assert insights.best_month == "2026-02"


def test_run_analytics_does_not_modify_input() -> None:
    dataframe = sample_dataframe()

    original_columns = dataframe.columns.tolist()

    run_analytics(dataframe)

    assert dataframe.columns.tolist() == original_columns

    assert "Revenue" not in dataframe.columns

    assert "Order_Size" not in dataframe.columns

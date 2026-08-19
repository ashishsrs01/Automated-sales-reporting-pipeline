import pandas as pd

from src.analytics.aggregations import (
    calculate_overall_metrics,
    revenue_by_region,
)


def test_overall_metrics() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": ["A", "B", "C"],
            "Quantity": [2, 3, 5],
            "Revenue": [100.0, 300.0, 500.0],
        }
    )

    result = calculate_overall_metrics(dataframe)

    assert result["total_revenue"] == 900.0
    assert result["total_orders"] == 3
    assert result["total_units"] == 10
    assert result["average_order_value"] == 300.0


def test_revenue_by_region() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": ["A", "B", "C"],
            "Region": ["North", "South", "North"],
            "Quantity": [2, 3, 5],
            "Revenue": [100.0, 300.0, 500.0],
        }
    )

    result = revenue_by_region(dataframe)

    assert result["Region"].tolist() == [
        "North",
        "South",
    ]

    assert result["Revenue"].tolist() == [
        600.0,
        300.0,
    ]
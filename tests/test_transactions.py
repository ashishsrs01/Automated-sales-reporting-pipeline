import pandas as pd
import pytest

from src.analytics.transactions import (
    calculate_revenue,
    classify_order_size,
)


def test_calculate_revenue() -> None:
    dataframe = pd.DataFrame(
        {
            "Quantity": [2, 5, 10],
            "Unit_Price": [100.0, 200.0, 50.0],
        }
    )

    result = calculate_revenue(dataframe)

    assert result["Revenue"].tolist() == [
        200.0,
        1000.0,
        500.0,
    ]


def test_original_dataframe_is_not_modified() -> None:
    dataframe = pd.DataFrame(
        {
            "Quantity": [2],
            "Unit_Price": [100.0],
        }
    )

    calculate_revenue(dataframe)

    assert "Revenue" not in dataframe.columns


def test_missing_quantity_raises_error() -> None:
    dataframe = pd.DataFrame(
        {
            "Unit_Price": [100.0],
        }
    )

    with pytest.raises(ValueError, match="Quantity"):
        calculate_revenue(dataframe)


def test_missing_unit_price_raises_error() -> None:
    dataframe = pd.DataFrame(
        {
            "Quantity": [2],
        }
    )

    with pytest.raises(ValueError, match="Unit_Price"):
        calculate_revenue(dataframe)


def test_classify_order_size() -> None:
    dataframe = pd.DataFrame(
        {
            "Revenue": [
                499.0,
                500.0,
                1999.0,
                2000.0,
            ]
        }
    )

    result = classify_order_size(dataframe)

    assert result["Order_Size"].astype(str).tolist() == [
        "Small",
        "Medium",
        "Medium",
        "Large",
    ]

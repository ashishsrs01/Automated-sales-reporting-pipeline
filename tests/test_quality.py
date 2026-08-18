import pandas as pd

from src.ingestion.quality import (
    count_invalid_dates,
    count_invalid_order_ids,
    count_invalid_prices,
    count_invalid_quantities,
    count_invalid_regions,
    find_missing_values,
    validate_data_quality,
)


def test_missing_values() -> None:
    dataframe = pd.DataFrame(
        {
            "Customer_ID": ["CUST-0001", None],
            "Region": ["North", "South"],
        }
    )

    result = find_missing_values(dataframe)

    assert result == {"Customer_ID": 1}


def test_invalid_order_id() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "INVALID",
            ]
        }
    )

    assert count_invalid_order_ids(dataframe) == 1


def test_invalid_date() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": [
                "2026-01-15",
                "not-a-date",
            ]
        }
    )

    assert count_invalid_dates(dataframe) == 1


def test_invalid_region() -> None:
    dataframe = pd.DataFrame(
        {
            "Region": [
                "North",
                "north",
                "South",
            ]
        }
    )

    assert count_invalid_regions(dataframe) == 1


def test_invalid_quantity() -> None:
    dataframe = pd.DataFrame(
        {
            "Quantity": [1, 5, 0, -1, "invalid"]
        }
    )

    assert count_invalid_quantities(dataframe) == 3


def test_invalid_price() -> None:
    dataframe = pd.DataFrame(
        {
            "Unit_Price": [100.0, 500.0, 0, -50, "invalid"]
        }
    )

    assert count_invalid_prices(dataframe) == 3


def test_valid_dataset() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": ["ORD-202601-00001"],
            "Order_Date": ["2026-01-15"],
            "Region": ["North"],
            "Quantity": [2],
            "Unit_Price": [999.0],
        }
    )

    result = validate_data_quality(dataframe)

    assert result.is_valid is True
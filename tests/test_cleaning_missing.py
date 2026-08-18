import pandas as pd

from src.cleaning.missing import (
    fill_allowed_missing_values,
    handle_missing_and_invalid_records,
    remove_invalid_required_records,
)


def test_allowed_missing_values_are_filled() -> None:
    dataframe = pd.DataFrame(
        {
            "Customer_ID": ["CUST-001", None],
            "Region": ["North", None],
            "Salesperson": ["Alice", None],
        }
    )

    cleaned, count = fill_allowed_missing_values(dataframe)

    assert count == 3
    assert cleaned["Customer_ID"].iloc[1] == "Unknown"
    assert cleaned["Region"].iloc[1] == "Unknown"
    assert cleaned["Salesperson"].iloc[1] == "Unknown"


def test_invalid_required_records_are_removed() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "ORD-202601-00002",
                "ORD-202601-00003",
            ],
            "Order_Date": [
                pd.Timestamp("2026-01-01"),
                pd.NaT,
                pd.Timestamp("2026-01-03"),
            ],
            "Product": [
                "Laptop",
                "Mouse",
                None,
            ],
            "Quantity": [2, 3, -1],
            "Unit_Price": [1000.0, 500.0, 200.0],
        }
    )

    cleaned, removed = remove_invalid_required_records(
        dataframe
    )

    assert removed == 2
    assert len(cleaned) == 1


def test_complete_handling() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "ORD-202601-00002",
            ],
            "Order_Date": [
                pd.Timestamp("2026-01-01"),
                pd.NaT,
            ],
            "Product": [
                "Laptop",
                "Mouse",
            ],
            "Quantity": [2, 3],
            "Unit_Price": [1000.0, 500.0],
            "Customer_ID": ["CUST-001", None],
            "Region": ["North", None],
            "Salesperson": ["Alice", None],
        }
    )

    _, stats = handle_missing_and_invalid_records(
        dataframe
    )

    assert stats.rows_before == 2
    assert stats.rows_after == 1
    assert stats.rows_removed == 1
    assert stats.missing_values_filled == 3
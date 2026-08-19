import pandas as pd

from src.cleaning.text import (
    normalize_category,
    normalize_region,
    normalize_text,
    normalize_text_columns,
)


def test_normalize_text() -> None:
    assert normalize_text("  Laptop Stand  ") == "Laptop Stand"


def test_normalize_region() -> None:
    assert normalize_region(" north ") == "North"
    assert normalize_region("SOUTH") == "South"


def test_unknown_region() -> None:
    assert normalize_region("Nrth") == "Unknown"


def test_normalize_category() -> None:
    assert normalize_category(" electronics ") == "Electronics"
    assert normalize_category("OFFICE SUPPLIES") == "Office Supplies"


def test_unknown_category() -> None:
    assert normalize_category("Something Else") == "Unknown"


def test_normalize_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "Product": ["  Laptop Stand  "],
            "Category": [" electronics "],
            "Region": [" NORTH "],
            "Salesperson": ["  Alice  "],
            "Customer_ID": [" CUST-001 "],
        }
    )

    cleaned = normalize_text_columns(dataframe)

    assert cleaned.loc[0, "Product"] == "Laptop Stand"
    assert cleaned.loc[0, "Category"] == "Electronics"
    assert cleaned.loc[0, "Region"] == "North"
    assert cleaned.loc[0, "Salesperson"] == "Alice"
    assert cleaned.loc[0, "Customer_ID"] == "CUST-001"


def test_original_dataframe_is_not_modified() -> None:
    dataframe = pd.DataFrame(
        {
            "Region": [" north "],
        }
    )

    normalize_text_columns(dataframe)

    assert dataframe.loc[0, "Region"] == " north "

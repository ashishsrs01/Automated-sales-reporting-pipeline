import pandas as pd

from src.cleaning.dates import normalize_order_date


def test_date_conversion() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": [
                "2026-01-15",
                "15/01/2026",
                "01-15-2026",
            ]
        }
    )

    cleaned = normalize_order_date(dataframe)

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["Order_Date"]
    )

    assert cleaned["Order_Date"].notna().all()


def test_invalid_date_becomes_nat() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": [
                "2026-01-15",
                "not-a-date",
            ]
        }
    )

    cleaned = normalize_order_date(dataframe)

    assert cleaned["Order_Date"].notna().iloc[0]
    assert pd.isna(cleaned["Order_Date"].iloc[1])


def test_original_date_dataframe_is_not_modified() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": ["2026-01-15"],
        }
    )

    normalize_order_date(dataframe)

    assert dataframe["Order_Date"].iloc[0] == "2026-01-15"
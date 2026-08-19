import pandas as pd

from src.cleaning.numeric import normalize_numeric_columns


def test_numeric_conversion() -> None:
    dataframe = pd.DataFrame(
        {
            "Quantity": ["2", "5", "invalid"],
            "Unit_Price": ["100.50", "999", "bad"],
        }
    )

    cleaned = normalize_numeric_columns(dataframe)

    assert cleaned["Quantity"].iloc[0] == 2
    assert cleaned["Quantity"].iloc[1] == 5
    assert pd.isna(cleaned["Quantity"].iloc[2])

    assert cleaned["Unit_Price"].iloc[0] == 100.50
    assert cleaned["Unit_Price"].iloc[1] == 999
    assert pd.isna(cleaned["Unit_Price"].iloc[2])


def test_numeric_input_is_not_modified() -> None:
    dataframe = pd.DataFrame(
        {
            "Quantity": ["2"],
            "Unit_Price": ["100"],
        }
    )

    normalize_numeric_columns(dataframe)

    assert dataframe["Quantity"].iloc[0] == "2"

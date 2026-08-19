import pandas as pd


def normalize_quantity(dataframe):
    cleaned = dataframe.copy()
    if "Quantity" in cleaned.columns:
        cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce")
    return cleaned


def normalize_unit_price(dataframe):
    cleaned = dataframe.copy()
    if "Unit_Price" in cleaned.columns:
        cleaned["Unit_Price"] = pd.to_numeric(cleaned["Unit_Price"], errors="coerce")
    return cleaned


def normalize_numeric_columns(dataframe):
    cleaned = dataframe.copy()
    cleaned = normalize_quantity(cleaned)
    cleaned = normalize_unit_price(cleaned)
    return cleaned

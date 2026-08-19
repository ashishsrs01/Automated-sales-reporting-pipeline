import pandas as pd


def normalize_order_date(dataframe):
    cleaned = dataframe.copy()
    if "Order_Date" in cleaned.columns:
        cleaned["Order_Date"] = pd.to_datetime(
            cleaned["Order_Date"], errors="coerce", format="mixed"
        )
    return cleaned

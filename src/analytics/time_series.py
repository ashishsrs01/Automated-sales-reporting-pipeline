import pandas as pd


def calculate_monthly_metrics(dataframe):
    required_columns = {"Order_Date", "Order_ID", "Quantity", "Revenue"}
    missing_columns = required_columns - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    result = dataframe.copy()
    if not pd.api.types.is_datetime64_any_dtype(result["Order_Date"]):
        result["Order_Date"] = pd.to_datetime(result["Order_Date"], errors="coerce")
    if result["Order_Date"].isna().any():
        raise ValueError("Order_Date contains invalid or missing values.")
    result["Month"] = result["Order_Date"].dt.to_period("M")
    monthly = (
        result.groupby("Month")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Order_ID", "nunique"),
            Units=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("Month")
        .reset_index(drop=True)
    )
    return monthly


def calculate_mom_growth(monthly_dataframe):
    required_columns = {"Month", "Revenue"}
    missing_columns = required_columns - set(monthly_dataframe.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    result = monthly_dataframe.copy()
    result = result.sort_values("Month").reset_index(drop=True)
    previous_revenue = result["Revenue"].shift(1)
    result["MoM_Growth"] = result["Revenue"].div(previous_revenue).sub(1).mul(100)
    result.loc[previous_revenue == 0, "MoM_Growth"] = pd.NA
    return result

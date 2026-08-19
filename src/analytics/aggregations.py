

def calculate_overall_metrics(dataframe):
    required_columns = {"Order_ID", "Quantity", "Revenue"}
    missing_columns = required_columns - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    total_revenue = float(dataframe["Revenue"].sum())
    total_orders = int(dataframe["Order_ID"].nunique())
    total_units = int(dataframe["Quantity"].sum())
    average_order_value = total_revenue / total_orders if total_orders else 0.0
    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_units": total_units,
        "average_order_value": average_order_value,
    }


def revenue_by_dimension(dataframe, dimension):
    required_columns = {dimension, "Order_ID", "Quantity", "Revenue"}
    missing_columns = required_columns - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    return (
        dataframe.groupby(dimension, dropna=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Order_ID", "nunique"),
            Units=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )


def revenue_by_region(dataframe):
    return revenue_by_dimension(dataframe, "Region")


def revenue_by_category(dataframe):
    return revenue_by_dimension(dataframe, "Category")


def revenue_by_salesperson(dataframe):
    return revenue_by_dimension(dataframe, "Salesperson")


def revenue_by_product(dataframe):
    return revenue_by_dimension(dataframe, "Product")

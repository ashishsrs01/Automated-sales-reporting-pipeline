class BusinessInsights:
    def __init__(
        self,
        top_region,
        top_category,
        top_product,
        top_salesperson,
        best_month,
        worst_month,
        strongest_growth_month,
        strongest_growth_rate,
        largest_decline_month,
        largest_decline_rate,
    ):
        self.top_region = top_region
        self.top_category = top_category
        self.top_product = top_product
        self.top_salesperson = top_salesperson
        self.best_month = best_month
        self.worst_month = worst_month
        self.strongest_growth_month = strongest_growth_month
        self.strongest_growth_rate = strongest_growth_rate
        self.largest_decline_month = largest_decline_month
        self.largest_decline_rate = largest_decline_rate


def _top_dimension(dataframe, dimension):
    if dataframe.empty:
        return None
    if dimension not in dataframe.columns:
        raise ValueError(f"Missing required column: {dimension}")
    if "Revenue" not in dataframe.columns:
        raise ValueError("Missing required column: Revenue")
    grouped = (
        dataframe.groupby(dimension, dropna=False)["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    if grouped.empty:
        return None
    return str(grouped.index[0])


def top_region(dataframe):
    return _top_dimension(dataframe, "Region")


def top_category(dataframe):
    return _top_dimension(dataframe, "Category")


def top_product(dataframe):
    return _top_dimension(dataframe, "Product")


def top_salesperson(dataframe):
    return _top_dimension(dataframe, "Salesperson")


def best_revenue_month(monthly_dataframe):
    if monthly_dataframe.empty:
        return None
    required = {"Month", "Revenue"}
    missing = required - set(monthly_dataframe.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    index = monthly_dataframe["Revenue"].idxmax()
    return str(monthly_dataframe.loc[index, "Month"])


def worst_revenue_month(monthly_dataframe):
    if monthly_dataframe.empty:
        return None
    required = {"Month", "Revenue"}
    missing = required - set(monthly_dataframe.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    index = monthly_dataframe["Revenue"].idxmin()
    return str(monthly_dataframe.loc[index, "Month"])


def strongest_growth(monthly_dataframe):
    required = {"Month", "MoM_Growth"}
    missing = required - set(monthly_dataframe.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    valid = monthly_dataframe.dropna(subset=["MoM_Growth"])
    positive = valid[valid["MoM_Growth"] > 0]
    if positive.empty:
        return (None, None)
    index = positive["MoM_Growth"].idxmax()
    return (str(positive.loc[index, "Month"]), float(positive.loc[index, "MoM_Growth"]))


def largest_decline(monthly_dataframe):
    required = {"Month", "MoM_Growth"}
    missing = required - set(monthly_dataframe.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    valid = monthly_dataframe.dropna(subset=["MoM_Growth"])
    negative = valid[valid["MoM_Growth"] < 0]
    if negative.empty:
        return (None, None)
    index = negative["MoM_Growth"].idxmin()
    return (str(negative.loc[index, "Month"]), float(negative.loc[index, "MoM_Growth"]))


def generate_business_insights(dataframe, monthly_dataframe):
    growth_month, growth_rate = strongest_growth(monthly_dataframe)
    decline_month, decline_rate = largest_decline(monthly_dataframe)
    return BusinessInsights(
        top_region=top_region(dataframe),
        top_category=top_category(dataframe),
        top_product=top_product(dataframe),
        top_salesperson=top_salesperson(dataframe),
        best_month=best_revenue_month(monthly_dataframe),
        worst_month=worst_revenue_month(monthly_dataframe),
        strongest_growth_month=growth_month,
        strongest_growth_rate=growth_rate,
        largest_decline_month=decline_month,
        largest_decline_rate=decline_rate,
    )

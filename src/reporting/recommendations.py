from src.reporting.models import Recommendation


def generate_recommendations(dataframe, monthly_metrics, insights):
    recommendations = []
    if (
        insights.largest_decline_rate is not None
        and insights.largest_decline_rate < -10
    ):
        recommendations.append(
            Recommendation(
                title="Investigate revenue decline",
                description=f"Revenue declined by {abs(insights.largest_decline_rate):.1f}% in {insights.largest_decline_month} compared with the previous month.",
                severity="warning",
            )
        )
    regional_recommendation = _regional_concentration(dataframe)
    if regional_recommendation is not None:
        recommendations.append(regional_recommendation)
    category_recommendation = _category_concentration(dataframe)
    if category_recommendation is not None:
        recommendations.append(category_recommendation)
    return tuple(recommendations)


def _regional_concentration(dataframe):
    if dataframe.empty:
        return None
    required = {"Region", "Revenue"}
    if not required.issubset(dataframe.columns):
        return None
    regional_revenue = dataframe.groupby("Region")["Revenue"].sum()
    total_revenue = regional_revenue.sum()
    if total_revenue <= 0:
        return None
    top_region = regional_revenue.idxmax()
    share = regional_revenue.loc[top_region] / total_revenue * 100
    if share <= 50:
        return None
    return Recommendation(
        title="Monitor regional concentration",
        description=f"{top_region} contributes {share:.1f}% of total revenue. Consider monitoring dependence on this region.",
        severity="warning",
    )


def _category_concentration(dataframe):
    if dataframe.empty:
        return None
    required = {"Category", "Revenue"}
    if not required.issubset(dataframe.columns):
        return None
    category_revenue = dataframe.groupby("Category")["Revenue"].sum()
    total_revenue = category_revenue.sum()
    if total_revenue <= 0:
        return None
    top_category = category_revenue.idxmax()
    share = category_revenue.loc[top_category] / total_revenue * 100
    if share <= 60:
        return None
    return Recommendation(
        title="Monitor category concentration",
        description=f"{top_category} contributes {share:.1f}% of total revenue. Consider monitoring dependence on this category.",
        severity="warning",
    )

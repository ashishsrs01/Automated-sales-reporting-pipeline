import pandas as pd

from src.analytics.insights import BusinessInsights
from src.reporting.recommendations import (
    generate_recommendations,
)


def test_revenue_decline_recommendation() -> None:
    insights = BusinessInsights(
        top_region="North",
        top_category="Electronics",
        top_product="Laptop",
        top_salesperson="Alice",
        best_month="2026-03",
        worst_month="2026-02",
        strongest_growth_month="2026-03",
        strongest_growth_rate=15.0,
        largest_decline_month="2026-02",
        largest_decline_rate=-15.0,
    )

    recommendations = generate_recommendations(
        dataframe=pd.DataFrame(),
        monthly_metrics=pd.DataFrame(),
        insights=insights,
    )

    assert len(recommendations) == 1

    assert (
        recommendations[0].title
        == "Investigate revenue decline"
    )

    assert recommendations[0].severity == "warning"


def test_small_decline_does_not_trigger_warning() -> None:
    insights = BusinessInsights(
        top_region="North",
        top_category="Electronics",
        top_product="Laptop",
        top_salesperson="Alice",
        best_month="2026-03",
        worst_month="2026-02",
        strongest_growth_month="2026-03",
        strongest_growth_rate=15.0,
        largest_decline_month="2026-02",
        largest_decline_rate=-5.0,
    )

    recommendations = generate_recommendations(
        dataframe=pd.DataFrame(),
        monthly_metrics=pd.DataFrame(),
        insights=insights,
    )

    assert recommendations == ()

def test_regional_concentration() -> None:
    dataframe = pd.DataFrame(
        {
            "Region": [
                "North",
                "North",
                "South",
            ],
            "Revenue": [
                7000.0,
                1000.0,
                2000.0,
            ],
        }
    )

    insights = BusinessInsights(
        top_region="North",
        top_category=None,
        top_product=None,
        top_salesperson=None,
        best_month=None,
        worst_month=None,
        strongest_growth_month=None,
        strongest_growth_rate=None,
        largest_decline_month=None,
        largest_decline_rate=None,
    )

    recommendations = generate_recommendations(
        dataframe=dataframe,
        monthly_metrics=pd.DataFrame(),
        insights=insights,
    )

    assert any(
        recommendation.title
        == "Monitor regional concentration"
        for recommendation in recommendations
    )
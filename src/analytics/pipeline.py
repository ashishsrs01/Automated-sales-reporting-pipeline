from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .aggregations import (
    calculate_overall_metrics,
    revenue_by_category,
    revenue_by_product,
    revenue_by_region,
    revenue_by_salesperson,
)
from .insights import BusinessInsights, generate_business_insights
from .time_series import (
    calculate_mom_growth,
    calculate_monthly_metrics,
)
from .transactions import (
    calculate_revenue,
    classify_order_size,
)


@dataclass(frozen=True)
class AnalyticsResult:
    """Complete output produced by the analytics pipeline."""

    enriched_data: pd.DataFrame
    overall_metrics: dict[str, float | int]

    by_region: pd.DataFrame
    by_category: pd.DataFrame
    by_product: pd.DataFrame
    by_salesperson: pd.DataFrame

    monthly_metrics: pd.DataFrame
    business_insights: BusinessInsights


def run_analytics(
    dataframe: pd.DataFrame,
) -> AnalyticsResult:
    """Run the complete analytics pipeline."""

    # ---------------------------------------------------------
    # 1. Transaction-level enrichment
    # ---------------------------------------------------------
    enriched_data = calculate_revenue(dataframe)

    enriched_data = classify_order_size(
        enriched_data
    )

    # ---------------------------------------------------------
    # 2. Overall metrics
    # ---------------------------------------------------------
    overall_metrics = calculate_overall_metrics(
        enriched_data
    )

    # ---------------------------------------------------------
    # 3. Dimension aggregations
    # ---------------------------------------------------------
    by_region = revenue_by_region(
        enriched_data
    )

    by_category = revenue_by_category(
        enriched_data
    )

    by_product = revenue_by_product(
        enriched_data
    )

    by_salesperson = revenue_by_salesperson(
        enriched_data
    )

    # ---------------------------------------------------------
    # 4. Time-series metrics
    # ---------------------------------------------------------
    monthly_metrics = calculate_monthly_metrics(
        enriched_data
    )

    monthly_metrics = calculate_mom_growth(
        monthly_metrics
    )

    # ---------------------------------------------------------
    # 5. Business insights
    # ---------------------------------------------------------
    business_insights = generate_business_insights(
        enriched_data,
        monthly_metrics,
    )

    return AnalyticsResult(
        enriched_data=enriched_data,
        overall_metrics=overall_metrics,
        by_region=by_region,
        by_category=by_category,
        by_product=by_product,
        by_salesperson=by_salesperson,
        monthly_metrics=monthly_metrics,
        business_insights=business_insights,
    )
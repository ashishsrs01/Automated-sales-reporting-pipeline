import pandas as pd
from .aggregations import calculate_overall_metrics, revenue_by_category, revenue_by_product, revenue_by_region, revenue_by_salesperson
from .insights import BusinessInsights, generate_business_insights
from .time_series import calculate_mom_growth, calculate_monthly_metrics
from .transactions import calculate_revenue, classify_order_size

class AnalyticsResult:

    def __init__(self, enriched_data, overall_metrics, by_region, by_category, by_product, by_salesperson, monthly_metrics, business_insights):
        self.enriched_data = enriched_data
        self.overall_metrics = overall_metrics
        self.by_region = by_region
        self.by_category = by_category
        self.by_product = by_product
        self.by_salesperson = by_salesperson
        self.monthly_metrics = monthly_metrics
        self.business_insights = business_insights

def run_analytics(dataframe):
    enriched_data = calculate_revenue(dataframe)
    enriched_data = classify_order_size(enriched_data)
    overall_metrics = calculate_overall_metrics(enriched_data)
    by_region = revenue_by_region(enriched_data)
    by_category = revenue_by_category(enriched_data)
    by_product = revenue_by_product(enriched_data)
    by_salesperson = revenue_by_salesperson(enriched_data)
    monthly_metrics = calculate_monthly_metrics(enriched_data)
    monthly_metrics = calculate_mom_growth(monthly_metrics)
    business_insights = generate_business_insights(enriched_data, monthly_metrics)
    return AnalyticsResult(enriched_data=enriched_data, overall_metrics=overall_metrics, by_region=by_region, by_category=by_category, by_product=by_product, by_salesperson=by_salesperson, monthly_metrics=monthly_metrics, business_insights=business_insights)
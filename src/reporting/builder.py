from datetime import datetime, timezone

from src.reporting.models import KPISet, ReportData, ReportMetadata, ReportTables
from src.reporting.recommendations import generate_recommendations


def build_report_data(analytics_result):
    enriched_data = analytics_result.enriched_data
    if enriched_data.empty:
        raise ValueError("Cannot build a report from an empty dataset.")
    reporting_start = enriched_data["Order_Date"].min().strftime("%Y-%m-%d")
    reporting_end = enriched_data["Order_Date"].max().strftime("%Y-%m-%d")
    metadata = ReportMetadata(
        title="Business Performance Report",
        reporting_start=reporting_start,
        reporting_end=reporting_end,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
    overall = analytics_result.overall_metrics
    kpis = KPISet(
        total_revenue=float(overall["total_revenue"]),
        total_orders=int(overall["total_orders"]),
        total_units=int(overall["total_units"]),
        average_order_value=float(overall["average_order_value"]),
    )
    tables = ReportTables(
        by_region=analytics_result.by_region,
        by_category=analytics_result.by_category,
        by_product=analytics_result.by_product,
        by_salesperson=analytics_result.by_salesperson,
        monthly_metrics=analytics_result.monthly_metrics,
    )
    recommendations = generate_recommendations(
        dataframe=enriched_data,
        monthly_metrics=analytics_result.monthly_metrics,
        insights=analytics_result.business_insights,
    )
    return ReportData(
        metadata=metadata,
        kpis=kpis,
        tables=tables,
        insights=analytics_result.business_insights,
        recommendations=recommendations,
    )

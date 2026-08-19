report = build_report_data(
    analytics_result
)

assert report.metadata.title == (
    "Business Performance Report"
)

assert report.kpis.total_revenue > 0

assert report.kpis.total_orders > 0

assert not report.tables.by_region.empty

assert report.insights is not None

assert isinstance(
    report.recommendations,
    tuple,
)
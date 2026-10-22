class ReportMetadata:
    def __init__(self, title, reporting_start, reporting_end, generated_at):
        self.title = title
        self.reporting_start = reporting_start
        self.reporting_end = reporting_end
        self.generated_at = generated_at


class KPISet:
    def __init__(self, total_revenue, total_orders, total_units, average_order_value):
        self.total_revenue = total_revenue
        self.total_orders = total_orders
        self.total_units = total_units
        self.average_order_value = average_order_value


class ReportTables:
    def __init__(
        self, by_region, by_category, by_product, by_salesperson, monthly_metrics
    ):
        self.by_region = by_region
        self.by_category = by_category
        self.by_product = by_product
        self.by_salesperson = by_salesperson
        self.monthly_metrics = monthly_metrics


class Recommendation:
    def __init__(self, title, description, severity):
        self.title = title
        self.description = description
        self.severity = severity


class ReportData:
    def __init__(self, metadata, kpis, tables, insights, recommendations, quality=None):
        self.metadata = metadata
        self.kpis = kpis
        self.tables = tables
        self.insights = insights
        self.recommendations = recommendations
        self.quality = quality


class DataQualitySummary:
    def __init__(
        self,
        rows_before,
        rows_after,
        rows_removed,
        missing_values_filled,
        duplicates_removed,
    ):
        self.rows_before = rows_before
        self.rows_after = rows_after
        self.rows_removed = rows_removed
        self.missing_values_filled = missing_values_filled
        self.duplicates_removed = duplicates_removed

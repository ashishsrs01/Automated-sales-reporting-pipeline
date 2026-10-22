"""Export report calculations as JSON consumed by the GitHub Pages dashboard."""

import json
from calendar import monthrange
from datetime import date
from pathlib import Path


def _records(dataframe):
    if dataframe is None:
        return []
    normalized = dataframe.copy()
    if "Month" in normalized.columns:
        normalized["Month"] = normalized["Month"].astype(str)
    return json.loads(normalized.to_json(orient="records", date_format="iso"))


def build_dashboard_payload(report):
    """Return JSON-compatible content using the report's calculated values."""
    insights = report.insights
    quality = report.quality
    reporting_end = date.fromisoformat(report.metadata.reporting_end)
    latest_period_complete = (
        reporting_end.day == monthrange(reporting_end.year, reporting_end.month)[1]
    )
    return {
        "metadata": {
            "title": report.metadata.title,
            "reporting_start": report.metadata.reporting_start,
            "reporting_end": report.metadata.reporting_end,
            "generated_at": report.metadata.generated_at,
            "latest_period_complete": latest_period_complete,
        },
        "kpis": {
            "total_revenue": report.kpis.total_revenue,
            "total_orders": report.kpis.total_orders,
            "total_units": report.kpis.total_units,
            "average_order_value": report.kpis.average_order_value,
        },
        "monthly_metrics": _records(report.tables.monthly_metrics),
        "by_region": _records(report.tables.by_region),
        "by_category": _records(report.tables.by_category),
        "by_product": _records(report.tables.by_product),
        "by_salesperson": _records(report.tables.by_salesperson),
        "insights": {
            "top_region": insights.top_region,
            "top_category": insights.top_category,
            "top_product": insights.top_product,
            "top_salesperson": insights.top_salesperson,
            "best_month": insights.best_month,
            "worst_month": insights.worst_month,
            "strongest_growth_month": insights.strongest_growth_month,
            "strongest_growth_rate": insights.strongest_growth_rate,
            "largest_decline_month": insights.largest_decline_month,
            "largest_decline_rate": insights.largest_decline_rate,
        },
        "recommendations": [
            {
                "title": item.title,
                "description": item.description,
                "severity": item.severity,
            }
            for item in report.recommendations
        ],
        "quality": (
            {
                "rows_before": quality.rows_before,
                "rows_after": quality.rows_after,
                "rows_removed": quality.rows_removed,
                "missing_values_filled": quality.missing_values_filled,
                "duplicates_removed": quality.duplicates_removed,
            }
            if quality is not None
            else None
        ),
    }


def write_dashboard_data(report, output_path):
    """Write the static website's dashboard payload to ``output_path``."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_dashboard_payload(report), indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    return output_path

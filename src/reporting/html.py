from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd

from src.reporting.models import ReportData


def render_html_report(
    report: ReportData,
    charts: dict[str, Path],
    output_path: Path,
) -> Path:
    """Render report data and generated charts as a standalone HTML file."""
    chart_markup = "\n".join(
        f'<img class="chart" src="{escape(str(path))}" alt="{escape(name)}">'
        for name, path in charts.items()
    )

    kpis = "\n".join(
        (
            _kpi_card("Total revenue", _format_currency(report.kpis.total_revenue)),
            _kpi_card("Total orders", _format_integer(report.kpis.total_orders)),
            _kpi_card("Total units", _format_integer(report.kpis.total_units)),
            _kpi_card(
                "Average order value",
                _format_currency(report.kpis.average_order_value),
            ),
        )
    )

    insights = "\n".join(
        _insight_card("Business insight", description)
        for description in _build_insights(report)
    )

    recommendations = "\n".join(
        _recommendation_card(
            recommendation.title,
            recommendation.description,
            recommendation.severity,
        )
        for recommendation in report.recommendations
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(report.metadata.title)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ margin-bottom: 30px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
        .kpi-card, .insight-card, .recommendation-card {{ padding: 16px; border: 1px solid #ddd; border-radius: 8px; }}
        .kpi-label {{ font-size: 12px; text-transform: uppercase; }}
        .kpi-value {{ font-size: 24px; font-weight: bold; }}
        .section {{ margin-top: 40px; }}
        .chart {{ width: 100%; max-width: 900px; margin: 12px 0; }}
        .insights, .recommendations {{ display: grid; gap: 12px; }}
        .severity {{ font-size: 12px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <header class="header">
        <h1>{escape(report.metadata.title)}</h1>
        <p>{escape(report.metadata.reporting_start)} to {escape(report.metadata.reporting_end)}</p>
    </header>
    <section class="kpi-grid">{kpis}</section>
    <section class="section"><h2>Insights</h2><div class="insights">{insights}</div></section>
    <section class="section"><h2>Recommendations</h2><div class="recommendations">{recommendations}</div></section>
    <section class="section"><h2>Charts</h2>{chart_markup}</section>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _kpi_card(
    label: str,
    value: str,
) -> str:
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{escape(label)}</div>
        <div class="kpi-value">{escape(value)}</div>
    </div>
    """


def _format_currency(value: float) -> str:
    return f"₹{value:,.2f}"


def _format_integer(value: int) -> str:
    return f"{value:,}"


def _insight_card(title: str, description: str) -> str:
    return f"""
    <div class="insight-card">
        <h3>{escape(title)}</h3>
        <p>{escape(description)}</p>
    </div>
    """


def _build_insights(report: ReportData) -> list[str]:
    insights = report.insights
    results: list[str] = []

    if insights.top_region is not None:
        results.append(f"{insights.top_region} generated the highest revenue among regions.")

    if insights.top_category is not None:
        results.append(f"{insights.top_category} was the highest-revenue category.")

    if insights.best_month is not None:
        results.append(f"{insights.best_month} recorded the highest monthly revenue.")

    if (
        insights.strongest_growth_month is not None
        and insights.strongest_growth_rate is not None
    ):
        results.append(
            f"Revenue grew by {insights.strongest_growth_rate:.1f}% "
            f"in {insights.strongest_growth_month}."
        )

    return results


def _recommendation_card(title: str, description: str, severity: str) -> str:
    return f"""
    <div class="recommendation-card">
        <h3>{escape(title)}</h3>
        <p>{escape(description)}</p>
        <span class="severity">{escape(severity)}</span>
    </div>
    """


def _dataframe_to_html(dataframe: pd.DataFrame) -> str:
    return dataframe.to_html(index=False, classes="data-table", border=0)
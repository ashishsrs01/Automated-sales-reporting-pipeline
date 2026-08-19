from html import escape


def render_html_report(report, charts, output_path):
    chart_markup = "\n".join(
        (
            f'<img class="chart" src="{escape(str(path))}" alt="{escape(name)}">'
            for name, path in charts.items()
        )
    )
    kpis = "\n".join(
        (
            _kpi_card("Total revenue", _format_currency(report.kpis.total_revenue)),
            _kpi_card("Total orders", _format_integer(report.kpis.total_orders)),
            _kpi_card("Total units", _format_integer(report.kpis.total_units)),
            _kpi_card(
                "Average order value", _format_currency(report.kpis.average_order_value)
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
    html = f'<!doctype html>\n<html lang="en">\n<head>\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <title>{escape(report.metadata.title)}</title>\n    <style>\n        body {{ font-family: Arial, sans-serif; margin: 40px; }}\n        .header {{ margin-bottom: 30px; }}\n        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}\n        .kpi-card, .insight-card, .recommendation-card {{ padding: 16px; border: 1px solid #ddd; border-radius: 8px; }}\n        .kpi-label {{ font-size: 12px; text-transform: uppercase; }}\n        .kpi-value {{ font-size: 24px; font-weight: bold; }}\n        .section {{ margin-top: 40px; }}\n        .chart {{ width: 100%; max-width: 900px; margin: 12px 0; }}\n        .insights, .recommendations {{ display: grid; gap: 12px; }}\n        .severity {{ font-size: 12px; text-transform: uppercase; }}\n    </style>\n</head>\n<body>\n    <header class="header">\n        <h1>{escape(report.metadata.title)}</h1>\n        <p>{escape(report.metadata.reporting_start)} to {escape(report.metadata.reporting_end)}</p>\n    </header>\n    <section class="section"><h2>Executive Summary</h2><div class="kpi-grid">{kpis}</div></section>\n    <section class="section"><h2>Key Insights</h2><div class="insights">{insights}</div></section>\n    <section class="section"><h2>Recommendations</h2><div class="recommendations">{recommendations}</div></section>\n    <section class="section"><h2>Charts</h2>{chart_markup}</section>\n</body>\n</html>\n'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _kpi_card(label, value):
    return f'\n    <div class="kpi-card">\n        <div class="kpi-label">{escape(label)}</div>\n        <div class="kpi-value">{escape(value)}</div>\n    </div>\n    '


def _format_currency(value):
    return f"₹{value:,.2f}"


def _format_integer(value):
    return f"{value:,}"


def _insight_card(title, description):
    return f'\n    <div class="insight-card">\n        <h3>{escape(title)}</h3>\n        <p>{escape(description)}</p>\n    </div>\n    '


def _build_insights(report):
    insights = report.insights
    results = []
    if insights.top_region is not None:
        results.append(
            f"{insights.top_region} generated the highest revenue among regions."
        )
    if insights.top_category is not None:
        results.append(f"{insights.top_category} was the highest-revenue category.")
    if insights.best_month is not None:
        results.append(f"{insights.best_month} recorded the highest monthly revenue.")
    if (
        insights.strongest_growth_month is not None
        and insights.strongest_growth_rate is not None
    ):
        results.append(
            f"Revenue grew by {insights.strongest_growth_rate:.1f}% in {insights.strongest_growth_month}."
        )
    return results


def _recommendation_card(title, description, severity):
    return f'\n    <div class="recommendation-card">\n        <h3>{escape(title)}</h3>\n        <p>{escape(description)}</p>\n        <span class="severity">{escape(severity)}</span>\n    </div>\n    '


def _dataframe_to_html(dataframe):
    return dataframe.to_html(index=False, classes="data-table", border=0)

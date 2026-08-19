from html import escape
from pathlib import Path


def render_html_report(report, charts, output_path):
    output_path = Path(output_path)

    kpis = _build_kpis(report)
    highlights = _build_highlights(report)
    alerts = _build_alerts(report)
    recommendations = _build_recommendations(report)
    chart_markup = _build_chart_grid(charts, output_path)

    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{escape(report.metadata.title)}</title>

    <style>
        :root {{
            --bg: #f5f7fa;
            --surface: #ffffff;
            --surface-soft: #f8fafc;
            --border: #e5e7eb;
            --text: #111827;
            --muted: #6b7280;
            --primary: #2563eb;
            --primary-soft: #eff6ff;
            --success: #15803d;
            --success-soft: #f0fdf4;
            --warning: #b45309;
            --warning-soft: #fffbeb;
            --danger: #dc2626;
            --danger-soft: #fef2f2;
            --shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
            --radius: 14px;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            background: var(--bg);
            color: var(--text);
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                Arial,
                sans-serif;
            line-height: 1.5;
        }}

        .dashboard {{
            width: min(1400px, calc(100% - 40px));
            margin: 0 auto;
            padding: 32px 0 60px;
        }}

        /* ---------- Header ---------- */

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 24px;
            margin-bottom: 28px;
        }}

        .eyebrow {{
            margin: 0 0 6px;
            color: var(--primary);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        h1 {{
            margin: 0;
            font-size: clamp(28px, 4vw, 42px);
            line-height: 1.1;
            letter-spacing: -0.03em;
        }}

        .report-period {{
            margin: 8px 0 0;
            color: var(--muted);
            font-size: 14px;
        }}

        .header-badge {{
            padding: 9px 14px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: var(--surface);
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            white-space: nowrap;
        }}

        /* ---------- Generic ---------- */

        .section {{
            margin-top: 30px;
        }}

        .section-heading {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 16px;
            margin-bottom: 14px;
        }}

        .section-heading h2 {{
            margin: 0;
            font-size: 20px;
            letter-spacing: -0.01em;
        }}

        .section-heading p {{
            margin: 0;
            color: var(--muted);
            font-size: 13px;
        }}

        /* ---------- KPI cards ---------- */

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
        }}

        .kpi-card {{
            position: relative;
            overflow: hidden;
            padding: 22px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
        }}

        .kpi-card::before {{
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 4px;
            background: var(--primary);
        }}

        .kpi-label {{
            margin-bottom: 8px;
            color: var(--muted);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .kpi-value {{
            font-size: clamp(22px, 3vw, 30px);
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: -0.025em;
        }}

        .kpi-context {{
            margin-top: 8px;
            color: var(--muted);
            font-size: 12px;
        }}

        .kpi-danger::before {{
            background: var(--danger);
        }}

        .kpi-success::before {{
            background: var(--success);
        }}

        .kpi-warning::before {{
            background: var(--warning);
        }}

        /* ---------- Highlights ---------- */

        .highlight-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
        }}

        .highlight-card {{
            min-height: 145px;
            padding: 20px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
        }}

        .highlight-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            margin-bottom: 14px;
            border-radius: 10px;
            background: var(--primary-soft);
            font-size: 18px;
        }}

        .highlight-label {{
            color: var(--muted);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .highlight-value {{
            margin-top: 4px;
            font-size: 20px;
            font-weight: 800;
        }}

        .highlight-detail {{
            margin-top: 3px;
            color: var(--muted);
            font-size: 12px;
        }}

        /* ---------- Alerts ---------- */

        .alert {{
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: 18px;
            padding: 20px 22px;
            border: 1px solid #fecaca;
            border-radius: var(--radius);
            background: var(--danger-soft);
        }}

        .alert-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 46px;
            height: 46px;
            border-radius: 12px;
            background: #fee2e2;
            font-size: 22px;
        }}

        .alert-title {{
            margin: 0;
            font-size: 16px;
            font-weight: 800;
        }}

        .alert-description {{
            margin: 3px 0 0;
            color: #7f1d1d;
            font-size: 13px;
        }}

        .alert-badge {{
            padding: 6px 10px;
            border-radius: 999px;
            background: #fee2e2;
            color: var(--danger);
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.08em;
        }}

        .no-alert {{
            padding: 20px;
            border: 1px solid #bbf7d0;
            border-radius: var(--radius);
            background: var(--success-soft);
            color: var(--success);
            font-weight: 700;
        }}

        /* ---------- Charts ---------- */

        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
        }}

        .chart-card {{
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
        }}

        .chart-header {{
            padding: 17px 18px 0;
        }}

        .chart-title {{
            margin: 0;
            font-size: 15px;
            font-weight: 800;
        }}

        .chart-description {{
            margin: 3px 0 0;
            color: var(--muted);
            font-size: 11px;
        }}

        .chart-image {{
            display: block;
            width: 100%;
            height: auto;
            padding: 12px;
        }}

        /* ---------- Recommendations ---------- */

        .recommendation-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
        }}

        .recommendation-card {{
            padding: 20px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
        }}

        .recommendation-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
        }}

        .recommendation-title {{
            margin: 0;
            font-size: 15px;
            font-weight: 800;
        }}

        .severity {{
            flex-shrink: 0;
            padding: 5px 8px;
            border-radius: 999px;
            background: var(--warning-soft);
            color: var(--warning);
            font-size: 9px;
            font-weight: 900;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .recommendation-description {{
            margin: 10px 0 0;
            color: var(--muted);
            font-size: 13px;
        }}

        /* ---------- Footer ---------- */

        .footer {{
            margin-top: 40px;
            padding-top: 18px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 11px;
            text-align: center;
        }}

        /* ---------- Responsive ---------- */

        @media (max-width: 1050px) {{
            .kpi-grid,
            .highlight-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 760px) {{
            .dashboard {{
                width: min(100% - 24px, 1400px);
                padding-top: 20px;
            }}

            .header {{
                align-items: flex-start;
                flex-direction: column;
            }}

            .kpi-grid,
            .highlight-grid,
            .chart-grid,
            .recommendation-grid {{
                grid-template-columns: 1fr;
            }}

            .alert {{
                grid-template-columns: auto 1fr;
            }}

            .alert-badge {{
                grid-column: 2;
                width: fit-content;
            }}
        }}
    </style>
</head>

<body>
<div class="dashboard">

    <header class="header">
        <div>
            <p class="eyebrow">Executive Dashboard</p>
            <h1>{escape(report.metadata.title)}</h1>
            <p class="report-period">
                {escape(report.metadata.reporting_start)}
                &nbsp;—&nbsp;
                {escape(report.metadata.reporting_end)}
            </p>
        </div>

        <div class="header-badge">
            Automated Business Intelligence Report
        </div>
    </header>

    <section class="section">
        <div class="section-heading">
            <h2>Performance at a Glance</h2>
            <p>Key business metrics for the reporting period</p>
        </div>

        <div class="kpi-grid">
            {kpis}
        </div>
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>What Matters Most</h2>
            <p>Fast answers from the underlying analysis</p>
        </div>

        <div class="highlight-grid">
            {highlights}
        </div>
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>Attention Required</h2>
            <p>Issues that may require business action</p>
        </div>

        {alerts}
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>Business Performance</h2>
            <p>Visual breakdown of the most important drivers</p>
        </div>

        <div class="chart-grid">
            {chart_markup}
        </div>
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>Recommended Actions</h2>
            <p>Prioritized actions generated from the analysis</p>
        </div>

        <div class="recommendation-grid">
            {recommendations}
        </div>
    </section>

    <footer class="footer">
        Generated automatically from the sales analytics pipeline.
    </footer>

</div>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _build_kpis(report):
    overall = report.kpis

    mom_growth = _get_latest_mom_growth(report)

    if mom_growth is None:
        growth_value = "N/A"
        growth_context = "Month-over-month change unavailable"
        growth_class = ""
    else:
        growth_value = _format_percentage(mom_growth)
        growth_context = "Latest month vs previous month"

        if mom_growth < 0:
            growth_class = "kpi-danger"
        elif mom_growth > 0:
            growth_class = "kpi-success"
        else:
            growth_class = "kpi-warning"

    return "\n".join(
        [
            _kpi_card(
                "Total Revenue",
                _format_currency(overall.total_revenue),
                "Revenue generated",
            ),
            _kpi_card(
                "Total Orders",
                _format_integer(overall.total_orders),
                "Orders processed",
            ),
            _kpi_card(
                "Average Order Value",
                _format_currency(overall.average_order_value),
                "Average revenue per order",
            ),
            _kpi_card(
                "Latest MoM Growth",
                growth_value,
                growth_context,
                css_class=growth_class,
            ),
        ]
    )


def _build_highlights(report):
    insights = report.insights
    tables = report.tables

    cards = []

    top_region = _top_row(tables.by_region, "Revenue")
    if top_region is not None:
        region = _safe_value(top_region, "Region")
        revenue = _safe_number(top_region, "Revenue")
        cards.append(
            _highlight_card(
                "🏆",
                "TOP REGION",
                region,
                _format_currency(revenue),
            )
        )

    top_category = _top_row(tables.by_category, "Revenue")
    if top_category is not None:
        category = _safe_value(top_category, "Category")
        revenue = _safe_number(top_category, "Revenue")
        cards.append(
            _highlight_card(
                "📦",
                "TOP CATEGORY",
                category,
                _format_currency(revenue),
            )
        )

    if insights.best_month is not None:
        best_month_revenue = _best_month_revenue(report)
        cards.append(
            _highlight_card(
                "📈",
                "BEST MONTH",
                str(insights.best_month),
                (
                    _format_currency(best_month_revenue)
                    if best_month_revenue is not None
                    else "Highest revenue"
                ),
            )
        )

    if (
        insights.strongest_growth_month is not None
        and insights.strongest_growth_rate is not None
    ):
        cards.append(
            _highlight_card(
                "🚀",
                "STRONGEST GROWTH",
                str(insights.strongest_growth_month),
                _format_percentage(insights.strongest_growth_rate),
            )
        )
    else:
        cards.append(
            _highlight_card(
                "📊",
                "PRODUCT RANGE",
                str(len(tables.by_product)),
                "Products analyzed",
            )
        )

    return "\n".join(cards)


def _build_alerts(report):
    mom_growth = _get_latest_mom_growth(report)

    if mom_growth is not None and mom_growth < 0:
        latest_month = _latest_month(report)
        previous_revenue = _previous_month_revenue(report)
        latest_revenue = _latest_month_revenue(report)

        if latest_month is not None:
            description = (
                f"Revenue fell by {_format_percentage(abs(mom_growth))} "
                f"in {latest_month} compared with the previous month."
            )

            if previous_revenue is not None and latest_revenue is not None:
                description += (
                    f" Revenue moved from "
                    f"{_format_currency(previous_revenue)} to "
                    f"{_format_currency(latest_revenue)}."
                )

            return f"""
                <div class="alert">
                    <div class="alert-icon">⚠️</div>
                    <div>
                        <p class="alert-title">Revenue decline detected</p>
                        <p class="alert-description">
                            {escape(description)}
                        </p>
                    </div>
                    <div class="alert-badge">HIGH PRIORITY</div>
                </div>
            """

    return """
        <div class="no-alert">
            ✓ No major negative month-over-month revenue signal detected.
        </div>
    """


def _build_recommendations(report):
    if not report.recommendations:
        return """
            <div class="recommendation-card">
                <p class="recommendation-description">
                    No specific recommendations were generated for this period.
                </p>
            </div>
        """

    return "\n".join(
        f"""
        <article class="recommendation-card">
            <div class="recommendation-top">
                <h3 class="recommendation-title">
                    {escape(str(recommendation.title))}
                </h3>
                <span class="severity">
                    {escape(str(recommendation.severity))}
                </span>
            </div>

            <p class="recommendation-description">
                {escape(str(recommendation.description))}
            </p>
        </article>
        """
        for recommendation in report.recommendations
    )


def _build_chart_grid(charts, output_path):
    chart_information = {
        "monthly_revenue": (
            "Revenue Trend",
            "Monthly revenue movement across the reporting period.",
        ),
        "revenue_by_region": (
            "Revenue by Region",
            "Compare regional contribution to total revenue.",
        ),
        "revenue_by_category": (
            "Revenue by Category",
            "Identify the categories driving business performance.",
        ),
        "top_products": (
            "Top Products",
            "Highest-revenue products in the current dataset.",
        ),
        "salesperson_revenue": (
            "Revenue by Salesperson",
            "Compare revenue contribution across salespeople.",
        ),
    }

    cards = []

    for name, chart_path in charts.items():
        title, description = chart_information.get(
            name,
            (name.replace("_", " ").title(), "Business performance visualization."),
        )

        relative_path = _relative_chart_path(chart_path, output_path)

        cards.append(
            f"""
            <article class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">{escape(title)}</h3>
                    <p class="chart-description">{escape(description)}</p>
                </div>

                <img
                    class="chart-image"
                    src="{escape(relative_path)}"
                    alt="{escape(title)}"
                    loading="lazy"
                >
            </article>
            """
        )

    return "\n".join(cards)


def _kpi_card(label, value, context, css_class=""):
    return f"""
        <article class="kpi-card {escape(css_class)}">
            <div class="kpi-label">{escape(label)}</div>
            <div class="kpi-value">{escape(str(value))}</div>
            <div class="kpi-context">{escape(context)}</div>
        </article>
    """


def _highlight_card(icon, label, value, detail):
    return f"""
        <article class="highlight-card">
            <div class="highlight-icon">{escape(icon)}</div>
            <div class="highlight-label">{escape(label)}</div>
            <div class="highlight-value">{escape(str(value))}</div>
            <div class="highlight-detail">{escape(str(detail))}</div>
        </article>
    """


def _format_currency(value):
    return f"₹{float(value):,.2f}"


def _format_integer(value):
    return f"{int(value):,}"


def _format_percentage(value):
    return f"{float(value):+.1f}%"


def _top_row(dataframe, value_column):
    if dataframe is None or dataframe.empty:
        return None

    if value_column not in dataframe.columns:
        return None

    return dataframe.loc[dataframe[value_column].idxmax()]


def _safe_value(row, column):
    if column not in row.index:
        return "Unknown"

    value = row[column]

    if value is None:
        return "Unknown"

    return str(value)


def _safe_number(row, column):
    if column not in row.index:
        return 0.0

    value = row[column]

    if value is None:
        return 0.0

    return float(value)


def _get_latest_mom_growth(report):
    dataframe = report.tables.monthly_metrics

    if dataframe is None or dataframe.empty:
        return None

    possible_columns = (
        "MoM_Growth",
        "MoM_Growth_Rate",
        "mom_growth",
        "mom_growth_rate",
        "Growth",
    )

    growth_column = next(
        (column for column in possible_columns if column in dataframe.columns),
        None,
    )

    if growth_column is None:
        return None

    valid = dataframe[growth_column].dropna()

    if valid.empty:
        return None

    return float(valid.iloc[-1])


def _latest_month(report):
    dataframe = report.tables.monthly_metrics

    if dataframe is None or dataframe.empty or "Month" not in dataframe.columns:
        return None

    return str(dataframe.iloc[-1]["Month"])


def _latest_month_revenue(report):
    dataframe = report.tables.monthly_metrics

    if dataframe is None or dataframe.empty or "Revenue" not in dataframe.columns:
        return None

    return float(dataframe.iloc[-1]["Revenue"])


def _previous_month_revenue(report):
    dataframe = report.tables.monthly_metrics

    if dataframe is None or len(dataframe) < 2 or "Revenue" not in dataframe.columns:
        return None

    return float(dataframe.iloc[-2]["Revenue"])


def _best_month_revenue(report):
    dataframe = report.tables.monthly_metrics

    if dataframe is None or dataframe.empty:
        return None

    if "Revenue" not in dataframe.columns:
        return None

    return float(dataframe["Revenue"].max())


def _relative_chart_path(chart_path, output_path):
    chart_path = Path(chart_path)
    output_path = Path(output_path)

    try:
        return str(chart_path.relative_to(output_path.parent))
    except ValueError:
        return str(Path("charts") / chart_path.name)

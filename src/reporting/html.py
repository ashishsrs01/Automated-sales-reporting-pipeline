from html import escape
from pathlib import Path


def render_html_report(report, charts, output_path):
    output_path = Path(output_path)

    kpis = _build_kpis(report)
    highlights = _build_highlights(report)
    alerts = _build_alerts(report)
    recommendations = _build_recommendations(report)
    hero_chart = _build_hero_chart(charts, output_path)
    chart_markup = _build_chart_grid(charts, output_path)

    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(report.metadata.title)}</title>

    <style>
        :root {{
            --bg: #eaf0f8;
            --surface: rgba(255,255,255,.68);
            --surface-soft: rgba(255,255,255,.46);
            --border: rgba(255,255,255,.78);
            --text: #1e293b;
            --muted: #64748b;
            --primary: #3b82f6;
            --primary-soft: #eff6ff;
            --success: #10b981;
            --success-soft: #d1fae5;
            --warning: #f59e0b;
            --warning-soft: #fef3c7;
            --danger: #ef4444;
            --danger-soft: #fee2e2;
            --shadow: 0 22px 50px -28px rgba(30,58,95,.42), 0 3px 12px rgba(30,58,95,.06);
            --shadow-hover: 0 26px 56px -26px rgba(30,58,95,.48), 0 8px 18px rgba(30,58,95,.08);
            --radius: 20px;
        }}

        * {{ box-sizing: border-box; }}

        body {{
            margin: 0;
            background:
                linear-gradient(135deg, rgba(255,255,255,.6), transparent 42%),
                linear-gradient(315deg, rgba(191,219,254,.42), transparent 48%),
                var(--bg);
            background-attachment: fixed;
            color: var(--text);
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, Arial, sans-serif;
            line-height: 1.45;
        }}

        .dashboard {{
            width: min(1480px, calc(100% - 40px));
            margin: 0 auto;
            padding: 28px 0 54px;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 24px;
            margin-bottom: 22px;
        }}

        .eyebrow {{
            margin: 0 0 5px;
            color: var(--primary);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
        }}

        h1 {{
            margin: 0;
            font-size: clamp(26px, 3.2vw, 38px);
            line-height: 1.08;
            letter-spacing: -.035em;
        }}

        .report-period {{
            margin: 7px 0 0;
            color: var(--muted);
            font-size: 13px;
        }}

        .header-badge {{
            padding: 9px 13px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: rgba(255,255,255,.5);
            box-shadow: 0 8px 20px rgba(30,58,95,.07);
            backdrop-filter: blur(14px);
            color: var(--muted);
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }}

        .section {{ margin-top: 20px; }}

        .section-heading {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 10px;
        }}

        .section-heading h2 {{
            margin: 0;
            font-size: 15px;
            letter-spacing: -.01em;
        }}

        .section-heading p {{
            margin: 0;
            color: var(--muted);
            font-size: 11px;
        }}

        /* KPI strip — compact, like a modern BI dashboard */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
        }}

        .kpi-card {{
            position: relative;
            overflow: hidden;
            min-height: 120px;
            padding: 20px 24px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .kpi-card::after {{
            content: "";
            position: absolute;
            right: -24px;
            bottom: -30px;
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: rgba(147,197,253,.23);
            filter: blur(1px);
        }}

        .kpi-label {{
            position: relative;
            z-index: 1;
            color: var(--muted);
            font-size: 13px;
            font-weight: 600;
        }}

        .kpi-value {{
            position: relative;
            z-index: 1;
            margin-top: 8px;
            font-size: clamp(24px, 3vw, 32px);
            font-weight: 800;
            line-height: 1.1;
            color: var(--text);
        }}

        .kpi-context {{
            position: relative;
            z-index: 1;
            margin-top: 8px;
            font-size: 11px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 999px;
            width: max-content;
        }}

        .kpi-danger .kpi-context {{ background: var(--danger-soft); color: var(--danger); }}
        .kpi-success .kpi-context {{ background: var(--success-soft); color: var(--success); }}
        .kpi-warning .kpi-context {{ background: var(--warning-soft); color: var(--warning); }}

        /* Main visual hierarchy */
        .hero-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.75fr) minmax(270px, .75fr);
            gap: 14px;
        }}

        .panel {{
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition: transform .2s ease, box-shadow .2s ease;
        }}

        .panel:hover,
        .chart-card:hover,
        .recommendation-card:hover,
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }}

        .hero-panel {{
            min-height: 350px;
            overflow: hidden;
        }}

        .hero-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
            padding: 18px 20px 4px;
        }}

        .hero-title {{
            margin: 0;
            font-size: 16px;
            font-weight: 800;
        }}

        .hero-description {{
            margin: 3px 0 0;
            color: var(--muted);
            font-size: 11px;
        }}

        .hero-badge {{
            padding: 5px 8px;
            border-radius: 999px;
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 9px;
            font-weight: 800;
            white-space: nowrap;
        }}

        .hero-chart {{
            display: block;
            width: 100%;
            height: auto;
            padding: 6px 12px 12px;
        }}

        .side-panel {{
            padding: 18px;
        }}

        .side-panel h3 {{
            margin: 0;
            font-size: 14px;
        }}

        .side-subtitle {{
            margin: 4px 0 14px;
            color: var(--muted);
            font-size: 10px;
        }}

        .highlight-list {{
            display: grid;
            gap: 9px;
        }}

        .highlight-card {{
            display: grid;
            grid-template-columns: 42px 1fr auto;
            align-items: center;
            gap: 12px;
            min-height: 64px;
            padding: 12px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,.58);
            background: var(--surface-soft);
            box-shadow: inset 0 1px rgba(255,255,255,.55);
            backdrop-filter: blur(12px);
        }}

        .highlight-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 10px;
            background: var(--primary-soft);
            font-size: 15px;
        }}

        .highlight-label {{
            color: var(--muted);
            font-size: 8px;
            font-weight: 800;
            letter-spacing: .07em;
        }}

        .highlight-value {{
            margin-top: 1px;
            font-size: 12px;
            font-weight: 800;
        }}

        .highlight-detail {{
            color: var(--muted);
            font-size: 9px;
            text-align: right;
        }}

        /* Risk callout */
        .alert {{
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: 13px;
            padding: 13px 16px;
            border: 1px solid #ffd4d4;
            border-radius: 14px;
            background: rgba(254,226,226,.66);
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
        }}

        .alert-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: #ffe0e0;
            font-size: 17px;
        }}

        .alert-title {{
            margin: 0;
            font-size: 13px;
            font-weight: 800;
        }}

        .alert-description {{
            margin: 2px 0 0;
            color: #8b3333;
            font-size: 10px;
        }}

        .alert-badge {{
            padding: 5px 8px;
            border-radius: 999px;
            background: #ffe0e0;
            color: var(--danger);
            font-size: 8px;
            font-weight: 900;
            letter-spacing: .07em;
        }}

        .no-alert {{
            padding: 13px 16px;
            border: 1px solid #c8eddf;
            border-radius: 14px;
            background: rgba(209,250,229,.62);
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
            color: var(--success);
            font-size: 11px;
            font-weight: 700;
        }}

        /* Supporting visuals */
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
        }}

        .chart-card {{
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition: transform .2s ease, box-shadow .2s ease;
        }}

        .chart-card:first-child {{
            grid-column: span 2;
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 12px;
            padding: 14px 16px 0;
        }}

        .chart-title {{
            margin: 0;
            font-size: 13px;
            font-weight: 800;
        }}

        .chart-description {{
            margin: 2px 0 0;
            color: var(--muted);
            font-size: 9px;
        }}

        .chart-image {{
            display: block;
            width: 100%;
            height: auto;
            padding: 6px 10px 10px;
        }}

        /* Recommendations are intentionally compact */
        .recommendation-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
        }}

        .recommendation-card {{
            padding: 20px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition: transform .2s ease, box-shadow .2s ease;
        }}

        .recommendation-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }}

        .recommendation-title {{
            margin: 0;
            font-size: 12px;
            font-weight: 800;
        }}

        .severity {{
            flex-shrink: 0;
            padding: 4px 7px;
            border-radius: 999px;
            background: var(--warning-soft);
            color: var(--warning);
            font-size: 8px;
            font-weight: 900;
            letter-spacing: .07em;
            text-transform: uppercase;
        }}

        .recommendation-description {{
            margin: 7px 0 0;
            color: var(--muted);
            font-size: 10px;
        }}

        .recommendation-actions {{
            margin-top: 9px;
            padding: 9px 11px;
            border-radius: 9px;
            border: 1px solid rgba(255,255,255,.55);
            background: var(--surface-soft);
            box-shadow: inset 0 1px rgba(255,255,255,.5);
        }}

        .recommendation-actions-title {{
            margin: 0 0 4px;
            color: var(--text);
            font-size: 8px;
            font-weight: 800;
            letter-spacing: .06em;
            text-transform: uppercase;
        }}

        .recommendation-actions ul {{
            margin: 0;
            padding-left: 15px;
            color: var(--muted);
            font-size: 9px;
        }}

        .recommendation-actions li {{ margin: 2px 0; }}

        .footer {{
            margin-top: 30px;
            padding-top: 14px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 9px;
            text-align: center;
        }}

        @media (max-width: 1050px) {{
            .hero-grid {{ grid-template-columns: 1fr; }}
            .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        }}

        @media (max-width: 760px) {{
            .dashboard {{
                width: min(100% - 20px, 1480px);
                padding-top: 18px;
            }}

            .header {{
                align-items: flex-start;
                flex-direction: column;
            }}

            .kpi-grid,
            .chart-grid,
            .recommendation-grid {{
                grid-template-columns: 1fr;
            }}

            .chart-card:first-child {{ grid-column: span 1; }}

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
            <p class="eyebrow">Sales Intelligence</p>
            <h1>{escape(report.metadata.title)}</h1>
            <p class="report-period">
                {escape(report.metadata.reporting_start)}
                &nbsp;—&nbsp;
                {escape(report.metadata.reporting_end)}
            </p>
        </div>

        <div class="header-badge">Automated Executive Dashboard</div>
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
        <div class="hero-grid">
            <article class="panel hero-panel">
                <div class="hero-header">
                    <div>
                        <h2 class="hero-title">Revenue & Sales Trend</h2>
                        <p class="hero-description">
                            Monthly revenue movement across the reporting period.
                        </p>
                    </div>
                    <span class="hero-badge">TREND</span>
                </div>

                {hero_chart}
            </article>

            <aside class="panel side-panel">
                <h3>What Matters Most</h3>
                <p class="side-subtitle">The strongest signals from the analysis</p>
                <div class="highlight-list">
                    {highlights}
                </div>
            </aside>
        </div>
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>Attention Required</h2>
            <p>Business risks detected by the pipeline</p>
        </div>
        {alerts}
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>Business Breakdown</h2>
            <p>Key drivers behind sales performance</p>
        </div>

        <div class="chart-grid" id="supporting-charts">
            {chart_markup}
        </div>
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>Recommended Actions</h2>
            <p>Prioritized next steps from the analysis</p>
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
    recommendations = []

    # Preserve recommendations generated by the analytics layer.
    for recommendation in report.recommendations:
        title = str(recommendation.title)
        severity = str(recommendation.severity)
        description = str(recommendation.description)

        actions = _recommendation_actions(
            title,
            description,
            report,
        )

        action_markup = _action_list(actions)

        recommendations.append(
            f"""
            <article class="recommendation-card">
                <div class="recommendation-top">
                    <h3 class="recommendation-title">
                        {escape(title)}
                    </h3>
                    <span class="severity">
                        {escape(severity)}
                    </span>
                </div>

                <p class="recommendation-description">
                    {escape(description)}
                </p>

                {action_markup}
            </article>
            """
        )

    # Add a data-quality recommendation when Unknown values exist.
    unknown_findings = _unknown_data_quality_findings(report)

    if unknown_findings:
        recommendations.append(
            f"""
            <article class="recommendation-card">
                <div class="recommendation-top">
                    <h3 class="recommendation-title">
                        Review Unknown data
                    </h3>
                    <span class="severity">
                        DATA QUALITY
                    </span>
                </div>

                <p class="recommendation-description">
                    Missing dimension values are present in the reporting data
                    and should be investigated before using the report for
                    operational decisions.
                </p>

                {_action_list(unknown_findings)}
            </article>
            """
        )

    if not recommendations:
        return """
            <div class="recommendation-card">
                <p class="recommendation-description">
                    No specific recommendations were generated for this period.
                </p>
            </div>
        """

    return "\n".join(recommendations)


def _recommendation_actions(title, description, report):
    text = f"{title} {description}".lower()
    actions = []

    if "revenue" in text and (
        "decline" in text or "drop" in text or "decrease" in text
    ):
        actions.extend(
            [
                "Compare the latest month with the previous month by region.",
                "Identify categories and products contributing to the decline.",
                "Verify that the latest month's source data is complete.",
            ]
        )

    if not actions:
        actions.append(
            "Review the underlying metrics and validate the finding before taking action."
        )

    return actions


def _action_list(actions):
    items = "\n".join(f"<li>{escape(str(action))}</li>" for action in actions)

    return f"""
        <div class="recommendation-actions">
            <p class="recommendation-actions-title">
                Recommended next steps
            </p>
            <ul>
                {items}
            </ul>
        </div>
    """


def _unknown_data_quality_findings(report):
    findings = []

    dimension_tables = (
        ("Category", report.tables.by_category),
        ("Region", report.tables.by_region),
        ("Salesperson", report.tables.by_salesperson),
    )

    for dimension_name, dataframe in dimension_tables:
        if dataframe is None or dataframe.empty:
            continue

        required_columns = {dimension_name, "Revenue"}

        if not required_columns.issubset(dataframe.columns):
            continue

        unknown_rows = dataframe[
            dataframe[dimension_name].astype(str).str.strip().str.lower().eq("unknown")
        ]

        if unknown_rows.empty:
            continue

        unknown_revenue = unknown_rows["Revenue"].sum()

        findings.append(
            f"{dimension_name}: "
            f"{_format_currency(unknown_revenue)} "
            "is associated with Unknown values."
        )

    if findings:
        findings.append(
            "Trace the affected source records and populate the missing dimension values."
        )

    return findings


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
        if name == "monthly_revenue":
            continue

        title, description = chart_information.get(
            name,
            (name.replace("_", " ").title(), "Business performance visualization."),
        )

        relative_path = _relative_chart_path(chart_path, output_path)

        cards.append(
            f"""
            <article class="chart-card">
                <div class="chart-header">
                    <div>
                        <h3 class="chart-title">{escape(title)}</h3>
                        <p class="chart-description">{escape(description)}</p>
                    </div>
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


def _build_hero_chart(charts, output_path):
    chart_path = charts.get("monthly_revenue")

    if chart_path is None:
        return """
            <div style="padding:24px;color:#7b8494;font-size:12px;">
                Revenue trend chart unavailable.
            </div>
        """

    relative_path = _relative_chart_path(chart_path, output_path)

    return f"""
        <img
            class="chart-image hero-chart"
            src="{escape(relative_path)}"
            alt="Revenue Trend"
            loading="eager"
        >
    """


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

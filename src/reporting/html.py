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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --surface: rgba(30, 41, 59, 0.7);
            --surface-hover: rgba(51, 65, 85, 0.8);
            --border: rgba(148, 163, 184, 0.15);
            --border-hover: rgba(148, 163, 184, 0.3);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #818cf8;
            --accent-glow: rgba(129, 140, 248, 0.5);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.15);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.15);
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.15);
            --radius-lg: 24px;
            --radius-md: 16px;
            --radius-sm: 8px;
            --shadow-sm: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
            --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.2), 0 10px 10px -5px rgba(0,0,0,0.1);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(16, 185, 129, 0.1), transparent 25%);
            background-attachment: fixed;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}

        .glass-panel {{
            background: var(--surface);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .glass-panel:hover {{
            border-color: var(--border-hover);
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }}

        .dashboard-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border);
        }}

        .eyebrow {{
            font-family: 'Outfit', sans-serif;
            color: var(--accent);
            font-size: 0.875rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            display: block;
        }}

        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: clamp(2rem, 4vw, 3.5rem);
            font-weight: 800;
            line-height: 1.1;
            background: linear-gradient(to right, #f8fafc, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}

        .report-period {{
            color: var(--text-muted);
            font-size: 1rem;
            font-weight: 500;
        }}

        .header-badge {{
            padding: 0.75rem 1.25rem;
            background: rgba(129, 140, 248, 0.1);
            border: 1px solid rgba(129, 140, 248, 0.3);
            border-radius: var(--radius-sm);
            color: var(--accent);
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.875rem;
            letter-spacing: 0.05em;
            box-shadow: 0 0 20px var(--accent-glow);
        }}

        .bento-grid {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1.5rem;
        }}

        .kpi-section {{
            grid-column: span 12;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
        }}

        .kpi-card {{
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: var(--border);
            transition: background 0.3s ease;
        }}
        .kpi-card:hover::before {{ background: var(--accent); }}
        
        .kpi-card.kpi-success:hover::before {{ background: var(--success); }}
        .kpi-card.kpi-danger:hover::before {{ background: var(--danger); }}
        .kpi-card.kpi-warning:hover::before {{ background: var(--warning); }}

        .kpi-label {{
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 1rem 0;
            color: var(--text-main);
        }}

        .kpi-context {{
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.35rem 0.75rem;
            border-radius: var(--radius-sm);
            width: fit-content;
        }}

        .kpi-success .kpi-context {{ background: var(--success-bg); color: var(--success); border: 1px solid rgba(16,185,129,0.2); }}
        .kpi-danger .kpi-context {{ background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(239,68,68,0.2); }}
        .kpi-warning .kpi-context {{ background: var(--warning-bg); color: var(--warning); border: 1px solid rgba(245,158,11,0.2); }}
        .kpi-neutral .kpi-context {{ background: rgba(148,163,184,0.1); color: var(--text-muted); }}

        .hero-chart-container {{
            grid-column: span 8;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
        }}

        .highlights-sidebar {{
            grid-column: span 4;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            background: linear-gradient(145deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
        }}

        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}

        .section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .section-subtitle {{
            color: var(--text-muted);
            font-size: 0.875rem;
        }}

        .badge-subtle {{
            background: var(--surface-hover);
            color: var(--accent);
            padding: 0.25rem 0.75rem;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .chart-image-wrap {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            border-radius: var(--radius-sm);
            background: #ffffff;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }}

        .chart-image {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}

        .highlight-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            border-radius: var(--radius-sm);
            background: rgba(255,255,255,0.03);
            margin-bottom: 1rem;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }}
        
        .highlight-item:hover {{
            background: rgba(255,255,255,0.06);
            border-color: var(--border);
            transform: translateX(4px);
        }}

        .highlight-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(129, 140, 248, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: inset 0 0 10px rgba(129, 140, 248, 0.1);
        }}

        .highlight-content {{
            flex: 1;
        }}

        .highlight-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}

        .highlight-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .highlight-detail {{
            font-size: 0.75rem;
            color: var(--accent);
            margin-top: 0.125rem;
        }}

        .alerts-section {{ grid-column: span 12; }}

        .alert-card {{
            display: flex;
            align-items: center;
            gap: 1.5rem;
            padding: 1.5rem;
            border-radius: var(--radius-md);
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .alert-card::before {{
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0; width: 4px;
            background: var(--danger);
        }}

        .alert-icon {{
            font-size: 2rem;
            background: rgba(239, 68, 68, 0.2);
            width: 64px; height: 64px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 16px;
            flex-shrink: 0;
        }}

        .alert-content h4 {{ margin-bottom: 0.25rem; color: #fca5a5; font-size: 1.125rem; font-family: 'Outfit', sans-serif; }}
        .alert-content p {{ color: var(--text-muted); font-size: 0.875rem; }}

        .alert-success {{
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}
        .alert-success::before {{ background: var(--success); }}
        .alert-success .alert-icon {{ background: rgba(16, 185, 129, 0.15); font-size: 1.5rem; color: var(--success); }}
        .alert-success .alert-content p {{ color: var(--success); font-weight: 500; font-size: 1rem; }}

        .small-chart-card {{
            grid-column: span 6;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
        }}

        .recommendations-section {{
            grid-column: span 12;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }}

        .rec-card {{
            padding: 1.5rem;
            background: linear-gradient(180deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8));
        }}

        .rec-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}
        
        .rec-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .rec-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 99px;
            font-size: 0.65rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            background: var(--warning-bg);
            color: var(--warning);
            border: 1px solid rgba(245,158,11,0.3);
        }}

        .rec-desc {{
            color: var(--text-muted);
            font-size: 0.875rem;
            margin-bottom: 1.25rem;
        }}

        .rec-actions {{
            background: rgba(0,0,0,0.2);
            border-radius: var(--radius-sm);
            padding: 1.25rem;
            border: 1px solid var(--border);
        }}

        .rec-actions-title {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 0.75rem;
        }}

        .rec-actions ul {{
            list-style: none;
        }}

        .rec-actions li {{
            font-size: 0.875rem;
            color: var(--text-muted);
            padding: 0.5rem 0 0.5rem 1.5rem;
            position: relative;
        }}

        .rec-actions li::before {{
            content: '→';
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: bold;
        }}

        footer {{
            text-align: center;
            padding-top: 3rem;
            color: var(--text-muted);
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}

        @media (max-width: 1024px) {{
            .hero-chart-container {{ grid-column: span 12; }}
            .highlights-sidebar {{ grid-column: span 12; display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }}
            .small-chart-card {{ grid-column: span 12; }}
        }}
        @media (max-width: 640px) {{
            .highlights-sidebar {{ grid-template-columns: 1fr; }}
            .header {{ flex-direction: column; align-items: flex-start; gap: 1rem; }}
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        
        <header class="header">
            <div>
                <span class="eyebrow">Sales Intelligence</span>
                <h1>{escape(report.metadata.title)}</h1>
                <div class="report-period">
                    {escape(report.metadata.reporting_start)} &nbsp;&bull;&nbsp; {escape(report.metadata.reporting_end)}
                </div>
            </div>
            <div class="header-badge">
                EXECUTIVE DASHBOARD
            </div>
        </header>

        <main class="bento-grid">
            <section class="kpi-section" aria-label="Performance at a Glance">
                {kpis}
            </section>

            <section class="hero-chart-container glass-panel">
                <div class="section-header">
                    <div>
                        <h2 class="section-title">Revenue & Sales Trend</h2>
                        <p class="section-subtitle">Monthly revenue movement across the reporting period</p>
                    </div>
                    <span class="badge-subtle">TREND</span>
                </div>
                <div class="chart-image-wrap">
                    {hero_chart}
                </div>
            </section>

            <aside class="highlights-sidebar glass-panel">
                <div class="section-header" style="margin-bottom: 2rem;">
                    <div>
                        <h2 class="section-title" style="font-size: 1.125rem;">What Matters Most</h2>
                        <p class="section-subtitle">Strongest analytical signals</p>
                    </div>
                </div>
                {highlights}
            </aside>

            <section class="alerts-section" aria-label="Attention Required">
                {alerts}
            </section>

            {chart_markup}

            <section class="recommendations-section">
                <div style="grid-column: 1 / -1; margin-bottom: -0.5rem;">
                    <h2 class="section-title" style="font-size: 1.5rem;">Recommended Actions</h2>
                    <p class="section-subtitle">Prioritized next steps from the analysis</p>
                </div>
                {recommendations}
            </section>
        </main>

        <footer>
            GENERATED AUTOMATICALLY BY SALES ANALYTICS PIPELINE &bull; {escape(report.metadata.reporting_end)}
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
        growth_class = "kpi-neutral"
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
                f"Revenue fell by {abs(float(mom_growth)):.1f}% "
                f"in {latest_month} compared with the previous month."
            )

            if previous_revenue is not None and latest_revenue is not None:
                description += (
                    f" Revenue moved from "
                    f"{_format_currency_full(previous_revenue)} to "
                    f"{_format_currency_full(latest_revenue)}."
                )

            return f"""
                <div class="alert-card">
                    <div class="alert-icon">⚠️</div>
                    <div class="alert-content">
                        <h4>Revenue decline detected</h4>
                        <p>{escape(description)}</p>
                    </div>
                    <span class="badge-subtle" style="position:absolute; top:1.5rem; right:1.5rem; background: rgba(239, 68, 68, 0.2); color: #f87171;">HIGH PRIORITY</span>
                </div>
            """

    return """
        <div class="alert-card alert-success">
            <div class="alert-icon">✓</div>
            <div class="alert-content">
                <p>No major negative month-over-month revenue signal detected.</p>
            </div>
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
            <article class="rec-card glass-panel">
                <div class="rec-header">
                    <h3 class="rec-title">
                        {escape(title)}
                    </h3>
                    <span class="rec-badge">
                        {escape(severity)}
                    </span>
                </div>

                <p class="rec-desc">
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
            <article class="rec-card glass-panel">
                <div class="rec-header">
                    <h3 class="rec-title">
                        Review Unknown data
                    </h3>
                    <span class="rec-badge">
                        DATA QUALITY
                    </span>
                </div>

                <p class="rec-desc">
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
            <div class="rec-card glass-panel">
                <p class="rec-desc">
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
        <div class="rec-actions">
            <p class="rec-actions-title">
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
            <article class="small-chart-card glass-panel">
                <div class="section-header" style="margin-bottom: 1rem;">
                    <div>
                        <h3 class="section-title" style="font-size: 1.125rem;">{escape(title)}</h3>
                        <p class="section-subtitle" style="font-size: 0.75rem;">{escape(description)}</p>
                    </div>
                </div>
                <div class="chart-image-wrap">
                    <img
                        class="chart-image"
                        src="{escape(relative_path)}"
                        alt="{escape(title)}"
                        loading="lazy"
                    >
                </div>
            </article>
            """
        )

    return "\n".join(cards)


def _build_hero_chart(charts, output_path):
    chart_path = charts.get("monthly_revenue")

    if chart_path is None:
        return """
            <div style="padding:24px;color:var(--text-muted);font-size:12px;">
                Revenue trend chart unavailable.
            </div>
        """

    relative_path = _relative_chart_path(chart_path, output_path)

    return f"""
        <img
            class="chart-image"
            src="{escape(relative_path)}"
            alt="Revenue Trend"
            loading="eager"
        >
    """


def _kpi_card(label, value, context, css_class=""):
    if not css_class:
        css_class = "kpi-neutral"
    return f"""
        <article class="kpi-card glass-panel {escape(css_class)}">
            <div class="kpi-label">{escape(label)}</div>
            <div class="kpi-value">{escape(str(value))}</div>
            <div class="kpi-context">{escape(context)}</div>
        </article>
    """


def _highlight_card(icon, label, value, detail):
    return f"""
        <article class="highlight-item">
            <div class="highlight-icon">{escape(icon)}</div>
            <div class="highlight-content">
                <div class="highlight-label">{escape(label)}</div>
                <div class="highlight-value">{escape(str(value))}</div>
                <div class="highlight-detail">{escape(str(detail))}</div>
            </div>
        </article>
    """


def _format_currency(value):
    v = float(value)
    if v >= 1_00_00_000:  # >= 1 Cr
        return f"₹{v / 1_00_00_000:.2f} Cr"
    if v >= 1_00_000:  # >= 1 L
        return f"₹{v / 1_00_000:.2f} L"
    if v >= 1_000:  # >= 1 K
        return f"₹{v / 1_000:.2f} K"
    return f"₹{v:,.2f}"


def _format_currency_full(value):
    """Full precision currency — used in alert descriptions."""
    return f"₹{float(value):,.2f}"


def _format_integer(value):
    v = int(value)
    if v >= 1_000:
        return f"{v:,}"
    return str(v)


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

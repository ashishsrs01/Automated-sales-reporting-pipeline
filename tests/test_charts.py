from pathlib import Path

import matplotlib
import pandas as pd

from src.analytics.insights import BusinessInsights
from src.reporting.charts import (
    generate_all_charts,
    plot_top_products,
)
from src.reporting.models import (
    KPISet,
    Recommendation,
    ReportData,
    ReportMetadata,
    ReportTables,
)

matplotlib.use("Agg")


def sample_report() -> ReportData:
    insights = BusinessInsights(
        top_region="North",
        top_category="Electronics",
        top_product="Laptop",
        top_salesperson="Alice",
        best_month="2026-02",
        worst_month="2026-01",
        strongest_growth_month="2026-02",
        strongest_growth_rate=20.0,
        largest_decline_month=None,
        largest_decline_rate=None,
    )

    return ReportData(
        metadata=ReportMetadata(
            title="Business Performance Report",
            reporting_start="2026-01-01",
            reporting_end="2026-02-28",
            generated_at="2026-03-01T00:00:00+00:00",
        ),
        kpis=KPISet(
            total_revenue=6300.0,
            total_orders=10,
            total_units=25,
            average_order_value=630.0,
        ),
        tables=ReportTables(
            by_region=pd.DataFrame(
                {
                    "Region": ["North", "South"],
                    "Revenue": [4000.0, 2300.0],
                }
            ),
            by_category=pd.DataFrame(
                {
                    "Category": [
                        "Electronics",
                        "Furniture",
                    ],
                    "Revenue": [4500.0, 1800.0],
                }
            ),
            by_product=pd.DataFrame(
                {
                    "Product": [
                        "Laptop",
                        "Chair",
                        "Mouse",
                    ],
                    "Revenue": [
                        3000.0,
                        1800.0,
                        1500.0,
                    ],
                }
            ),
            by_salesperson=pd.DataFrame(
                {
                    "Salesperson": [
                        "Alice",
                        "Bob",
                    ],
                    "Revenue": [
                        4000.0,
                        2300.0,
                    ],
                }
            ),
            monthly_metrics=pd.DataFrame(
                {
                    "Month": [
                        "2026-01",
                        "2026-02",
                    ],
                    "Revenue": [
                        3000.0,
                        3300.0,
                    ],
                    "Orders": [
                        5,
                        5,
                    ],
                    "Units": [
                        12,
                        13,
                    ],
                    "MoM_Growth": [
                        None,
                        10.0,
                    ],
                }
            ),
        ),
        insights=insights,
        recommendations=(
            Recommendation(
                title="Test recommendation",
                description="Test description",
                severity="warning",
            ),
        ),
    )


def test_generate_all_charts(
    tmp_path: Path,
) -> None:
    report = sample_report()

    charts = generate_all_charts(
        report,
        tmp_path,
    )

    assert set(charts) == {
        "monthly_revenue",
        "revenue_by_region",
        "revenue_by_category",
        "top_products",
        "salesperson_revenue",
    }

    for path in charts.values():
        assert path.exists()
        assert path.suffix == ".png"
        assert path.stat().st_size > 0


def test_top_products_respects_limit(
    tmp_path: Path,
) -> None:
    report = sample_report()

    path = plot_top_products(
        report,
        tmp_path,
        top_n=2,
    )

    assert path.exists()

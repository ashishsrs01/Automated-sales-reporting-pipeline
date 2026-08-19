from pathlib import Path

from src.reporting.charts import generate_all_charts
from src.reporting.html import render_html_report
from tests.test_charts import sample_report


def test_render_html_report(
    tmp_path: Path,
) -> None:
    report = sample_report()

    charts = generate_all_charts(
        report,
        tmp_path / "charts",
    )

    output = tmp_path / "report.html"

    result = render_html_report(
        report,
        charts,
        output,
    )

    assert result == output
    assert output.exists()
    assert output.stat().st_size > 0

    html = output.read_text(encoding="utf-8")

    # Core report identity
    assert "Business Performance Report" in html

    # New executive dashboard sections
    assert "Performance at a Glance" in html
    assert "What Matters Most" in html
    assert "Attention Required" in html
    assert "Business Performance" in html
    assert "Recommended Actions" in html

    # KPI content
    assert "Total Revenue" in html
    assert "Total Orders" in html
    assert "Average Order Value" in html
    assert "Latest MoM Growth" in html

    # Dashboard visualization content
    assert "Revenue Trend" in html
    assert "Revenue by Region" in html
    assert "Revenue by Category" in html
    assert "Top Products" in html
    assert "Revenue by Salesperson" in html

    # Report recommendations should still be rendered
    assert report.recommendations is not None

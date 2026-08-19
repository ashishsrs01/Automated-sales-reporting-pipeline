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

    assert "Business Performance Report" in html
    assert "Executive Summary" in html
    assert "Key Insights" in html
    assert "Recommendations" in html

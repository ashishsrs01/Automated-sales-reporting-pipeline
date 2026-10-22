import json
from calendar import monthrange
from datetime import date
from pathlib import Path

from src.analytics.pipeline import run_analytics
from src.cleaning.pipeline import clean_dataset
from src.ingestion.reader import ingest_csv_directory
from src.reporting.builder import build_report_data
from src.reporting.static_site import build_dashboard_payload, write_dashboard_data


def test_static_dashboard_payload_uses_report_metrics(tmp_path):
    ingested = ingest_csv_directory(Path("data/raw"))
    cleaned = clean_dataset(ingested.dataframe)
    analytics = run_analytics(cleaned.dataframe)
    report = build_report_data(analytics, cleaned)

    payload = build_dashboard_payload(report)
    output_path = write_dashboard_data(report, tmp_path / "assets" / "dashboard.json")
    written = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["kpis"]["total_revenue"] == report.kpis.total_revenue
    assert payload["monthly_metrics"]
    assert payload["by_region"]
    assert payload["quality"]["rows_before"] == cleaned.rows_before
    report_end = date.fromisoformat(report.metadata.reporting_end)
    expected_complete = (
        report_end.day == monthrange(report_end.year, report_end.month)[1]
    )
    assert payload["metadata"]["latest_period_complete"] is expected_complete
    assert written == payload


def test_static_site_uses_relative_assets_and_no_remote_dependencies():
    html = Path("site/index.html").read_text(encoding="utf-8")
    script = Path("site/assets/js/dashboard.js").read_text(encoding="utf-8")

    assert 'href="assets/css/dashboard.css"' in html
    assert 'src="assets/js/dashboard.js"' in html
    assert 'fetch("assets/data/dashboard.json")' in script
    assert "https://" not in html

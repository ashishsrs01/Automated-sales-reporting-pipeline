from pathlib import Path

from src.analytics.pipeline import run_analytics
from src.cleaning.pipeline import clean_dataset
from src.ingestion.reader import ingest_csv_directory
from src.reporting.builder import build_report_data
from src.reporting.charts import generate_all_charts
from src.reporting.html import render_html_report
from src.reporting.static_site import write_dashboard_data

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORT_PATH = OUTPUT_DIR / "business-performance-report.html"
STATIC_DATA_PATH = PROJECT_ROOT / "site" / "assets" / "data" / "dashboard.json"


def generate_report() -> Path:
    """Run the complete sales reporting pipeline."""
    ingested = ingest_csv_directory(INPUT_DIR)
    cleaned = clean_dataset(ingested.dataframe)
    analytics_result = run_analytics(cleaned.dataframe)
    report = build_report_data(analytics_result, cleaned)
    charts = generate_all_charts(report, CHARTS_DIR)
    write_dashboard_data(report, STATIC_DATA_PATH)

    return render_html_report(
        report,
        charts,
        REPORT_PATH,
    )


if __name__ == "__main__":
    report_path = generate_report()
    print(f"Report generated: {report_path}")

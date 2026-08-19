from pathlib import Path

from src.analytics.pipeline import run_analytics
from src.cleaning.pipeline import clean_dataset
from src.ingestion.reader import ingest_csv_directory
from src.reporting.builder import build_report_data
from src.reporting.charts import generate_all_charts
from src.reporting.html import render_html_report

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORT_PATH = OUTPUT_DIR / "business-performance-report.html"


def generate_report() -> Path:
    """Run the complete sales reporting pipeline."""
    ingested = ingest_csv_directory(INPUT_DIR)
    cleaned = clean_dataset(ingested.dataframe)
    analytics_result = run_analytics(cleaned.dataframe)
    report = build_report_data(analytics_result)
    charts = generate_all_charts(report, CHARTS_DIR)

    return render_html_report(
        report,
        charts,
        REPORT_PATH,
    )


if __name__ == "__main__":
    report_path = generate_report()
    print(f"Report generated: {report_path}")

from pathlib import Path

from src.analytics.pipeline import run_analytics
from src.cleaning.pipeline import clean_dataset
from src.ingestion.reader import ingest_csv_directory
from src.reporting.builder import build_report_data


def test_build_report_data() -> None:
    ingested = ingest_csv_directory(Path("data/raw"))
    cleaned = clean_dataset(ingested.dataframe)
    analytics_result = run_analytics(cleaned.dataframe)

    report = build_report_data(analytics_result)

    assert report.metadata.title == ("Business Performance Report")

    assert report.kpis.total_revenue > 0

    assert report.kpis.total_orders > 0

    assert not report.tables.by_region.empty

    assert report.insights is not None

    assert isinstance(
        report.recommendations,
        tuple,
    )

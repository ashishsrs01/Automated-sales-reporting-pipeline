from src.ingestion.quality import DataQualityResult
from src.ingestion.report import (
    build_validation_report,
    format_validation_report,
)
from src.ingestion.validator import SchemaValidationResult


def test_invalid_report_status() -> None:
    schema_result = SchemaValidationResult(
        is_valid=True,
        missing_columns=(),
        unexpected_columns=(),
        duplicate_columns=(),
    )

    quality_result = DataQualityResult(
        missing_values={"Customer_ID": 5},
        invalid_order_ids=0,
        invalid_dates=2,
        invalid_regions=0,
        invalid_quantities=3,
        invalid_prices=0,
    )

    report = build_validation_report(
        files_processed=6,
        rows_processed=15000,
        schema_result=schema_result,
        quality_result=quality_result,
    )

    assert report.is_valid is False
    assert report.status == "NEEDS_CLEANING"


def test_valid_report_status() -> None:
    schema_result = SchemaValidationResult(
        is_valid=True,
        missing_columns=(),
        unexpected_columns=(),
        duplicate_columns=(),
    )

    quality_result = DataQualityResult(
        missing_values={},
        invalid_order_ids=0,
        invalid_dates=0,
        invalid_regions=0,
        invalid_quantities=0,
        invalid_prices=0,
    )

    report = build_validation_report(
        files_processed=6,
        rows_processed=15000,
        schema_result=schema_result,
        quality_result=quality_result,
    )

    assert report.is_valid is True
    assert report.status == "PASS"


def test_format_validation_report() -> None:
    schema_result = SchemaValidationResult(
        is_valid=True,
        missing_columns=(),
        unexpected_columns=(),
        duplicate_columns=(),
    )

    quality_result = DataQualityResult(
        missing_values={"Region": 10},
        invalid_order_ids=0,
        invalid_dates=5,
        invalid_regions=2,
        invalid_quantities=1,
        invalid_prices=0,
    )

    report = build_validation_report(
        files_processed=6,
        rows_processed=15000,
        schema_result=schema_result,
        quality_result=quality_result,
    )

    output = format_validation_report(report)

    assert "DATA QUALITY REPORT" in output
    assert "Files processed:       6" in output
    assert "Missing values:        10" in output
    assert "Status: NEEDS_CLEANING" in output
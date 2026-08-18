from __future__ import annotations

from dataclasses import dataclass

from .quality import DataQualityResult
from .validator import SchemaValidationResult


@dataclass(frozen=True)
class ValidationReport:
    """Combined report from schema and data-quality validation."""

    files_processed: int
    rows_processed: int
    schema_valid: bool
    missing_columns: tuple[str, ...]
    unexpected_columns: tuple[str, ...]
    duplicate_columns: tuple[str, ...]
    missing_values: dict[str, int]
    invalid_order_ids: int
    invalid_dates: int
    invalid_regions: int
    invalid_quantities: int
    invalid_prices: int

    @property
    def is_valid(self) -> bool:
        """Return whether the complete dataset passes validation."""
        return (
            self.schema_valid
            and not self.missing_columns
            and not self.unexpected_columns
            and not self.duplicate_columns
            and not self.missing_values
            and self.invalid_order_ids == 0
            and self.invalid_dates == 0
            and self.invalid_regions == 0
            and self.invalid_quantities == 0
            and self.invalid_prices == 0
        )

    @property
    def status(self) -> str:
        """Return a human-readable validation status."""
        return "PASS" if self.is_valid else "NEEDS_CLEANING"


def build_validation_report(
    *,
    files_processed: int,
    rows_processed: int,
    schema_result: SchemaValidationResult,
    quality_result: DataQualityResult,
) -> ValidationReport:
    """Build a unified validation report."""
    return ValidationReport(
        files_processed=files_processed,
        rows_processed=rows_processed,
        schema_valid=schema_result.is_valid,
        missing_columns=schema_result.missing_columns,
        unexpected_columns=schema_result.unexpected_columns,
        duplicate_columns=schema_result.duplicate_columns,
        missing_values=quality_result.missing_values,
        invalid_order_ids=quality_result.invalid_order_ids,
        invalid_dates=quality_result.invalid_dates,
        invalid_regions=quality_result.invalid_regions,
        invalid_quantities=quality_result.invalid_quantities,
        invalid_prices=quality_result.invalid_prices,
    )

def format_validation_report(
    report: ValidationReport,
) -> str:
    """Format the validation report for terminal output."""
    missing_total = sum(report.missing_values.values())

    return "\n".join(
        [
            "DATA QUALITY REPORT",
            "────────────────────────────",
            f"Files processed:       {report.files_processed}",
            f"Rows processed:        {report.rows_processed}",
            "",
            f"Missing values:        {missing_total}",
            f"Invalid Order IDs:     {report.invalid_order_ids}",
            f"Invalid dates:         {report.invalid_dates}",
            f"Invalid regions:       {report.invalid_regions}",
            f"Invalid quantities:    {report.invalid_quantities}",
            f"Invalid prices:        {report.invalid_prices}",
            "",
            f"Status: {report.status}",
            "────────────────────────────",
        ]
    )



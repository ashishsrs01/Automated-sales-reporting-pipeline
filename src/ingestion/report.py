from .quality import DataQualityResult
from .validator import SchemaValidationResult

class ValidationReport:

    def __init__(self, files_processed, rows_processed, schema_valid, missing_columns, unexpected_columns, duplicate_columns, missing_values, invalid_order_ids, invalid_dates, invalid_regions, invalid_quantities, invalid_prices):
        self.files_processed = files_processed
        self.rows_processed = rows_processed
        self.schema_valid = schema_valid
        self.missing_columns = missing_columns
        self.unexpected_columns = unexpected_columns
        self.duplicate_columns = duplicate_columns
        self.missing_values = missing_values
        self.invalid_order_ids = invalid_order_ids
        self.invalid_dates = invalid_dates
        self.invalid_regions = invalid_regions
        self.invalid_quantities = invalid_quantities
        self.invalid_prices = invalid_prices

    @property
    def is_valid(self):
        return self.schema_valid and (not self.missing_columns) and (not self.unexpected_columns) and (not self.duplicate_columns) and (not self.missing_values) and (self.invalid_order_ids == 0) and (self.invalid_dates == 0) and (self.invalid_regions == 0) and (self.invalid_quantities == 0) and (self.invalid_prices == 0)

    @property
    def status(self):
        return 'PASS' if self.is_valid else 'NEEDS_CLEANING'

def build_validation_report(*, files_processed, rows_processed, schema_result, quality_result):
    return ValidationReport(files_processed=files_processed, rows_processed=rows_processed, schema_valid=schema_result.is_valid, missing_columns=schema_result.missing_columns, unexpected_columns=schema_result.unexpected_columns, duplicate_columns=schema_result.duplicate_columns, missing_values=quality_result.missing_values, invalid_order_ids=quality_result.invalid_order_ids, invalid_dates=quality_result.invalid_dates, invalid_regions=quality_result.invalid_regions, invalid_quantities=quality_result.invalid_quantities, invalid_prices=quality_result.invalid_prices)

def format_validation_report(report):
    missing_total = sum(report.missing_values.values())
    return '\n'.join(['DATA QUALITY REPORT', '────────────────────────────', f'Files processed:       {report.files_processed}', f'Rows processed:        {report.rows_processed}', '', f'Missing values:        {missing_total}', f'Invalid Order IDs:     {report.invalid_order_ids}', f'Invalid dates:         {report.invalid_dates}', f'Invalid regions:       {report.invalid_regions}', f'Invalid quantities:    {report.invalid_quantities}', f'Invalid prices:        {report.invalid_prices}', '', f'Status: {report.status}', '────────────────────────────'])
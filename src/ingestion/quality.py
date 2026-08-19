import pandas as pd
VALID_REGIONS = frozenset({'North', 'South', 'East', 'West', 'Central'})
ORDER_ID_PATTERN = '^ORD-\\d{6}-\\d{5}$'

class DataQualityResult:

    def __init__(self, missing_values, invalid_order_ids, invalid_dates, invalid_regions, invalid_quantities, invalid_prices):
        self.missing_values = missing_values
        self.invalid_order_ids = invalid_order_ids
        self.invalid_dates = invalid_dates
        self.invalid_regions = invalid_regions
        self.invalid_quantities = invalid_quantities
        self.invalid_prices = invalid_prices

    @property
    def is_valid(self):
        return not any((self.invalid_order_ids, self.invalid_dates, self.invalid_regions, self.invalid_quantities, self.invalid_prices, sum(self.missing_values.values())))

def find_missing_values(dataframe):
    missing = dataframe.isna().sum()
    return {column: int(count) for column, count in missing.items() if count > 0}

def count_invalid_order_ids(dataframe):
    valid = dataframe['Order_ID'].astype('string').str.match(ORDER_ID_PATTERN, na=False)
    return int((~valid).sum())

def count_invalid_dates(dataframe):
    parsed = pd.to_datetime(dataframe['Order_Date'], errors='coerce', format='mixed')
    return int(parsed.isna().sum())

def count_invalid_regions(dataframe):
    valid = dataframe['Region'].isin(VALID_REGIONS)
    return int((~valid).sum())

def count_invalid_quantities(dataframe):
    numeric = pd.to_numeric(dataframe['Quantity'], errors='coerce')
    invalid = numeric.isna() | (numeric <= 0)
    return int(invalid.sum())

def count_invalid_prices(dataframe):
    numeric = pd.to_numeric(dataframe['Unit_Price'], errors='coerce')
    invalid = numeric.isna() | (numeric <= 0)
    return int(invalid.sum())

def validate_data_quality(dataframe):
    return DataQualityResult(missing_values=find_missing_values(dataframe), invalid_order_ids=count_invalid_order_ids(dataframe), invalid_dates=count_invalid_dates(dataframe), invalid_regions=count_invalid_regions(dataframe), invalid_quantities=count_invalid_quantities(dataframe), invalid_prices=count_invalid_prices(dataframe))
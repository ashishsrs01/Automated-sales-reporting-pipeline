import pandas as pd


class CorruptionStats:
    def __init__(
        self,
        duplicate_rows=0,
        missing_values=0,
        text_errors=0,
        date_errors=0,
        invalid_quantities=0,
        invalid_prices=0,
    ):
        self.duplicate_rows = duplicate_rows
        self.missing_values = missing_values
        self.text_errors = text_errors
        self.date_errors = date_errors
        self.invalid_quantities = invalid_quantities
        self.invalid_prices = invalid_prices


def inject_duplicates(dataframe, rng, rate=0.015):
    count = int(len(dataframe) * rate)
    if count == 0:
        return (dataframe, 0)
    duplicate_rows = dataframe.sample(
        n=count, random_state=int(rng.integers(0, 1000000))
    )
    result = pd.concat([dataframe, duplicate_rows], ignore_index=True)
    return (result, count)


def inject_missing_values(dataframe, rng, rate=0.02):
    result = dataframe.copy()
    columns = ("Customer_ID", "Salesperson", "Region")
    total_changes = 0
    for column in columns:
        count = int(len(result) * rate)
        indexes = rng.choice(result.index, size=count, replace=False)
        result.loc[indexes, column] = pd.NA
        total_changes += count
    return (result, total_changes)


def inject_text_errors(dataframe, rng, rate=0.02):
    result = dataframe.copy()
    columns = ("Category", "Region")
    total_changes = 0
    for column in columns:
        count = int(len(result) * rate)
        indexes = rng.choice(result.index, size=count, replace=False)
        for index in indexes:
            value = result.at[index, column]
            if pd.isna(value):
                continue
            mode = rng.integers(0, 3)
            if mode == 0:
                result.at[index, column] = str(value).lower()
            elif mode == 1:
                result.at[index, column] = f" {value}"
            else:
                result.at[index, column] = f"{value} "
            total_changes += 1
    return (result, total_changes)


def inject_date_errors(dataframe, rng, rate=0.01):
    result = dataframe.copy()
    count = int(len(result) * rate)
    if count == 0:
        return (result, 0)
    if "Order_Date" not in result.columns:
        return (result, 0)
    indexes = rng.choice(result.index, size=count, replace=False)
    result.loc[indexes, "Order_Date"] = pd.NaT
    return (result, count)


def inject_invalid_numbers(dataframe, rng, rate=0.005):
    result = dataframe.copy()
    count = int(len(result) * rate)
    quantity_indexes = rng.choice(result.index, size=count, replace=False)
    price_indexes = rng.choice(result.index, size=count, replace=False)
    result.loc[quantity_indexes, "Quantity"] = -1
    result.loc[price_indexes, "Unit_Price"] = -100
    return (result, count, count)


def corrupt_dataset(dataframe, rng):
    stats = CorruptionStats()
    result, stats.duplicate_rows = inject_duplicates(dataframe, rng)
    result, stats.missing_values = inject_missing_values(result, rng)
    result, stats.text_errors = inject_text_errors(result, rng)
    result, stats.date_errors = inject_date_errors(result, rng)
    result, stats.invalid_quantities, stats.invalid_prices = inject_invalid_numbers(
        result, rng
    )
    return (result, stats)

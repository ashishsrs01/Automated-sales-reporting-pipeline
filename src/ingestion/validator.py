REQUIRED_COLUMNS = frozenset(
    {
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product",
        "Category",
        "Region",
        "Salesperson",
        "Quantity",
        "Unit_Price",
    }
)


class SchemaValidationResult:
    def __init__(
        self, is_valid, missing_columns, unexpected_columns, duplicate_columns
    ):
        self.is_valid = is_valid
        self.missing_columns = missing_columns
        self.unexpected_columns = unexpected_columns
        self.duplicate_columns = duplicate_columns


def find_duplicate_columns(columns):
    duplicates = columns[columns.duplicated()].unique()
    return tuple(sorted(str(column) for column in duplicates))


def validate_schema(dataframe):
    columns = dataframe.columns
    missing_columns = tuple(sorted(REQUIRED_COLUMNS - set(columns)))
    unexpected_columns = tuple(sorted(set(columns) - REQUIRED_COLUMNS))
    duplicate_columns = find_duplicate_columns(columns)
    is_valid = not (
        bool(missing_columns) or bool(unexpected_columns) or bool(duplicate_columns)
    )
    return SchemaValidationResult(
        is_valid=is_valid,
        missing_columns=missing_columns,
        unexpected_columns=unexpected_columns,
        duplicate_columns=duplicate_columns,
    )

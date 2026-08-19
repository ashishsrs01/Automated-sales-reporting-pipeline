import pandas as pd

from src.ingestion.validator import (
    REQUIRED_COLUMNS,
    validate_schema,
)


def create_valid_dataframe() -> pd.DataFrame:
    """Create a DataFrame with the expected sales schema."""
    return pd.DataFrame(columns=sorted(REQUIRED_COLUMNS))


def test_valid_schema() -> None:
    dataframe = create_valid_dataframe()

    result = validate_schema(dataframe)

    assert result.is_valid is True
    assert result.missing_columns == ()
    assert result.unexpected_columns == ()
    assert result.duplicate_columns == ()


def test_missing_column() -> None:
    dataframe = create_valid_dataframe().drop(columns=["Region"])

    result = validate_schema(dataframe)

    assert result.is_valid is False
    assert result.missing_columns == ("Region",)


def test_unexpected_column() -> None:
    dataframe = create_valid_dataframe()
    dataframe["Unknown_Field"] = None

    result = validate_schema(dataframe)

    assert result.is_valid is False
    assert result.unexpected_columns == ("Unknown_Field",)


def test_empty_dataframe_is_invalid() -> None:
    dataframe = pd.DataFrame()

    result = validate_schema(dataframe)

    assert result.is_valid is False

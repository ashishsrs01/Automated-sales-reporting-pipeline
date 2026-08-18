from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class IngestionResult:
    """Result produced by the CSV ingestion stage."""

    dataframe: pd.DataFrame
    files_processed: tuple[str, ...]
    rows_processed: int


def discover_csv_files(input_dir: Path) -> list[Path]:
    """Return CSV files found in the input directory."""
    if not input_dir.exists():
        raise FileNotFoundError(
            f"Input directory does not exist: {input_dir}"
        )

    if not input_dir.is_dir():
        raise NotADirectoryError(
            f"Input path is not a directory: {input_dir}"
        )

    return sorted(input_dir.glob("*.csv"))


def read_csv_file(path: Path) -> pd.DataFrame:
    """Read one CSV file into a DataFrame."""
    if not path.exists():
        raise FileNotFoundError(f"CSV file does not exist: {path}")

    try:
        dataframe = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"CSV file is empty: {path}") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(f"Unable to parse CSV file: {path}") from exc

    if dataframe.empty:
        raise ValueError(f"CSV file contains no records: {path}")

    return dataframe


def ingest_csv_directory(input_dir: Path) -> IngestionResult:
    """Read and combine all CSV files from an input directory."""
    files = discover_csv_files(input_dir)

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in input directory: {input_dir}"
        )

    dataframes: list[pd.DataFrame] = []
    processed_files: list[str] = []

    for path in files:
        dataframe = read_csv_file(path)

        dataframe = dataframe.copy()
        dataframe["source_file"] = path.name

        dataframes.append(dataframe)
        processed_files.append(path.name)

    combined = pd.concat(
        dataframes,
        ignore_index=True,
    )

    return IngestionResult(
        dataframe=combined,
        files_processed=tuple(processed_files),
        rows_processed=len(combined),
    )

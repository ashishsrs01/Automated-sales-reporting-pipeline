import pandas as pd


class IngestionResult:
    def __init__(self, dataframe, files_processed, rows_processed):
        self.dataframe = dataframe
        self.files_processed = files_processed
        self.rows_processed = rows_processed


def discover_csv_files(input_dir):
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")
    return sorted(input_dir.glob("*.csv"))


def read_csv_file(path):
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


def ingest_csv_directory(input_dir):
    files = discover_csv_files(input_dir)
    if not files:
        raise FileNotFoundError(f"No CSV files found in input directory: {input_dir}")
    dataframes = []
    processed_files = []
    for path in files:
        dataframe = read_csv_file(path)
        dataframe = dataframe.copy()
        dataframe["source_file"] = path.name
        dataframes.append(dataframe)
        processed_files.append(path.name)
    combined = pd.concat(dataframes, ignore_index=True)
    return IngestionResult(
        dataframe=combined,
        files_processed=tuple(processed_files),
        rows_processed=len(combined),
    )

from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.reader import (
    discover_csv_files,
    ingest_csv_directory,
    read_csv_file,
)


def test_discover_csv_files(tmp_path: Path) -> None:
    (tmp_path / "a.csv").write_text("id,value\n1,10\n")
    (tmp_path / "b.csv").write_text("id,value\n2,20\n")
    (tmp_path / "notes.txt").write_text("ignore me")

    files = discover_csv_files(tmp_path)

    assert [path.name for path in files] == [
        "a.csv",
        "b.csv",
    ]


def test_read_csv_file(tmp_path: Path) -> None:
    path = tmp_path / "sales.csv"
    path.write_text("id,value\n1,100\n")

    dataframe = read_csv_file(path)

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 1
    assert list(dataframe.columns) == ["id", "value"]


def test_ingest_csv_directory(tmp_path: Path) -> None:
    (tmp_path / "january.csv").write_text(
        "Order_ID,Quantity\nORD-1,2\n"
    )
    (tmp_path / "february.csv").write_text(
        "Order_ID,Quantity\nORD-2,3\n"
    )

    result = ingest_csv_directory(tmp_path)

    assert result.files_processed == (
        "february.csv",
        "january.csv",
    )
    assert result.rows_processed == 2
    assert "source_file" in result.dataframe.columns


def test_missing_directory_raises() -> None:
    with pytest.raises(FileNotFoundError):
        discover_csv_files(Path("does_not_exist"))


def test_empty_csv_raises(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("")

    with pytest.raises(ValueError):
        read_csv_file(path)
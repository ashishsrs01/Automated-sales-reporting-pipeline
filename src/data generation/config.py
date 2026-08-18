from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen= True)
class DatasetConfig:
    seed: int = 42
    customers: int = 5000
    transactions_per_month: int = 5500

    output_dir: Path = Path('data/raw')
    metadata_dir: Path = Path('data/metadata')

    months: tuple[str, ...] = ("january", "february", "march","april","may","june")

from pathlib import Path


class DatasetConfig:
    def __init__(self):
        self.seed = 42
        self.customers = 5000
        self.transactions_per_month = 5500
        self.output_dir = Path("data/raw")
        self.metadata_dir = Path("data/metadata")
        self.months = ("january", "february", "march", "april", "may", "june")

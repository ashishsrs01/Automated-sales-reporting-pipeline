import json
import sys
from pathlib import Path
import numpy as np
try:
    from .config import DatasetConfig
    from .corruption import corrupt_dataset
    from .generator import generate_customer_ids, generate_monthly_sales
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from config import DatasetConfig
    from corruption import corrupt_dataset
    from generator import generate_customer_ids, generate_monthly_sales

def main():
    config = DatasetConfig()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    config.metadata_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(config.seed)
    customer_ids = generate_customer_ids(config.customers)
    ground_truth = {}
    for month_number, month_name in enumerate(config.months, start=1):
        clean_data = generate_monthly_sales(year=2026, month=month_number, transaction_count=config.transactions_per_month, customer_ids=customer_ids, rng=rng)
        corrupted_data, stats = corrupt_dataset(clean_data, rng)
        filename = f'sales_{month_name}.csv'
        output_path = config.output_dir / filename
        corrupted_data.to_csv(output_path, index=False)
        ground_truth[filename] = {'original_rows': len(clean_data), 'final_rows': len(corrupted_data), 'duplicate_rows': stats.duplicate_rows, 'missing_values': stats.missing_values, 'text_errors': stats.text_errors, 'date_errors': stats.date_errors, 'invalid_quantities': stats.invalid_quantities, 'invalid_prices': stats.invalid_prices}
    metadata_path = config.metadata_dir / 'data_quality_ground_truth.json'
    metadata_path.write_text(json.dumps(ground_truth, indent=2), encoding='utf-8')
    print('Dataset generation complete.')
    print(f'Raw data: {config.output_dir}')
    print(f'Metadata: {metadata_path}')
if __name__ == '__main__':
    main()
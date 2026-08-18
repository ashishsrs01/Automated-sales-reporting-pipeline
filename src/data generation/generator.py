from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .config import DatasetConfig
except ImportError:  # pragma: no cover - fallback for direct script execution
    sys.path.append(str(Path(__file__).resolve().parent))
    from config import DatasetConfig


PRODUCT_CATALOG = {
    "Electronics": {
        "Wireless Mouse": 799.0,
        "Keyboard": 1299.0,
        "Headphones": 2499.0,
        "Webcam": 1899.0,
    },
    "Accessories": {
        "Laptop Stand": 1499.0,
        "USB Hub": 899.0,
        "Mouse Pad": 399.0,
    },
    "Office": {
        "Notebook": 199.0,
        "Pen Set": 299.0,
        "Desk Organizer": 599.0,
    },
    "Furniture": {
        "Office Chair": 6999.0,
        "Study Table": 5499.0,
        "Monitor Stand": 1999.0,
    },
}

REGIONS = ("North", "South", "East", "West", "Central")

SALESPEOPLE = (
    "Amit",
    "Priya",
    "Rahul",
    "Neha",
    "Vikram",
    "Ananya",
    "Karan",
    "Sneha",
)


def generate_customer_ids(count: int) -> list[str]:
    """Generate deterministic customer identifiers."""
    return [f"CUST-{index:04d}" for index in range(1, count + 1)]


def generate_product_catalog() -> pd.DataFrame:
    """Return the product catalog as a DataFrame."""
    rows = [
        {
            "product": product,
            "category": category,
            "base_price": price,
        }
        for category, products in PRODUCT_CATALOG.items()
        for product, price in products.items()
    ]

    return pd.DataFrame(rows)


def generate_monthly_sales(
    *,
    year: int,
    month: int,
    transaction_count: int,
    customer_ids: list[str],
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate clean sales transactions for one month."""
    catalog = generate_product_catalog()

    selected_products = rng.choice(
        len(catalog),
        size=transaction_count,
    )

    selected_catalog = catalog.iloc[selected_products].reset_index(drop=True)

    quantities = rng.integers(
        low=1,
        high=8,
        size=transaction_count,
    )

    price_noise = rng.uniform(
        0.90,
        1.10,
        size=transaction_count,
    )

    dates = pd.date_range(
        start=datetime(year, month, 1, tzinfo=UTC),
        periods=31,
        freq="D",
    )

    order_dates = rng.choice(
        dates,
        size=transaction_count,
    )

    return pd.DataFrame(
        {
            "Order_ID": [
                f"ORD-{year}{month:02d}-{index:05d}"
                for index in range(1, transaction_count + 1)
            ],
            "Order_Date": order_dates,
            "Customer_ID": rng.choice(
                customer_ids,
                size=transaction_count,
            ),
            "Product": selected_catalog["product"],
            "Category": selected_catalog["category"],
            "Region": rng.choice(
                REGIONS,
                size=transaction_count,
            ),
            "Salesperson": rng.choice(
                SALESPEOPLE,
                size=transaction_count,
            ),
            "Quantity": quantities,
            "Unit_Price": (
                selected_catalog["base_price"].to_numpy()
                * price_noise
            ).round(2),
        }
    )


def generate_dataset(config: DatasetConfig) -> None:
    """Generate all clean monthly sales files."""
    config.output_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(config.seed)
    customer_ids = generate_customer_ids(config.customers)

    for month_number, month_name in enumerate(config.months, start=1):
        dataframe = generate_monthly_sales(
            year=2026,
            month=month_number,
            transaction_count=config.transactions_per_month,
            customer_ids=customer_ids,
            rng=rng,
        )

        output_path = config.output_dir / f"sales_{month_name}.csv"

        dataframe.to_csv(
            output_path,
            index=False,
        )
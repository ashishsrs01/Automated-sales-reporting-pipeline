import pandas as pd

from src.cleaning.pipeline import clean_dataset


def test_complete_cleaning_pipeline() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "ORD-202601-00001",
                "ORD-202601-00002",
                "ORD-202601-00003",
            ],
            "Order_Date": [
                "2026-01-15",
                "2026-01-15",
                "15/01/2026",
                "invalid",
            ],
            "Customer_ID": [
                " CUST-001 ",
                " CUST-001 ",
                None,
                "CUST-003",
            ],
            "Product": [
                " Laptop ",
                " Laptop ",
                " Mouse ",
                " Keyboard ",
            ],
            "Category": [
                " electronics ",
                " electronics ",
                " ELECTRONICS ",
                "electronics",
            ],
            "Region": [
                " north ",
                " north ",
                None,
                " SOUTH ",
            ],
            "Salesperson": [
                " Alice ",
                " Alice ",
                None,
                " Bob ",
            ],
            "Quantity": [
                "2",
                "2",
                "5",
                "-1",
            ],
            "Unit_Price": [
                "1000",
                "1000",
                "500",
                "200",
            ],
        }
    )

    result = clean_dataset(dataframe)

    assert result.rows_before == 4
    assert result.rows_after == 2
    assert result.rows_removed == 2
    assert result.duplicates_removed == 1
    assert result.missing_values_filled == 3

    assert result.dataframe["Region"].tolist() == [
        "North",
        "Unknown",
    ]

    assert result.dataframe["Quantity"].tolist() == [
        2,
        5,
    ]

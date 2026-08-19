import pandas as pd

from src.cleaning.duplicates import remove_duplicate_orders


def test_duplicate_orders_are_removed() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "ORD-202601-00001",
                "ORD-202601-00002",
            ],
            "Quantity": [2, 2, 5],
        }
    )

    cleaned, removed = remove_duplicate_orders(dataframe)

    assert removed == 1
    assert len(cleaned) == 2
    assert cleaned["Order_ID"].tolist() == [
        "ORD-202601-00001",
        "ORD-202601-00002",
    ]


def test_no_duplicates() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "ORD-202601-00002",
            ]
        }
    )

    cleaned, removed = remove_duplicate_orders(dataframe)

    assert removed == 0
    assert len(cleaned) == 2


def test_original_dataframe_is_not_modified() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_ID": [
                "ORD-202601-00001",
                "ORD-202601-00001",
            ]
        }
    )

    remove_duplicate_orders(dataframe)

    assert len(dataframe) == 2

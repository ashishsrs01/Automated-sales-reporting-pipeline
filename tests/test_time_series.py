import pandas as pd
import pytest

from src.analytics.time_series import (
    calculate_mom_growth,
    calculate_monthly_metrics,
)


def test_calculate_monthly_metrics() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": pd.to_datetime(
                [
                    "2026-01-15",
                    "2026-01-20",
                    "2026-02-10",
                    "2026-02-25",
                ]
            ),
            "Order_ID": [
                "A",
                "B",
                "C",
                "D",
            ],
            "Quantity": [2, 3, 4, 1],
            "Revenue": [
                200.0,
                300.0,
                400.0,
                100.0,
            ],
        }
    )

    result = calculate_monthly_metrics(dataframe)

    assert result["Month"].astype(str).tolist() == [
        "2026-01",
        "2026-02",
    ]

    assert result["Revenue"].tolist() == [
        500.0,
        500.0,
    ]

    assert result["Orders"].tolist() == [
        2,
        2,
    ]

    assert result["Units"].tolist() == [
        5,
        5,
    ]


def test_monthly_metrics_are_chronologically_sorted() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": pd.to_datetime(
                [
                    "2026-03-01",
                    "2026-01-01",
                    "2026-02-01",
                ]
            ),
            "Order_ID": ["C", "A", "B"],
            "Quantity": [1, 1, 1],
            "Revenue": [300.0, 100.0, 200.0],
        }
    )

    result = calculate_monthly_metrics(dataframe)

    assert result["Month"].astype(str).tolist() == [
        "2026-01",
        "2026-02",
        "2026-03",
    ]

def test_calculate_mom_growth() -> None:
    monthly = pd.DataFrame(
        {
            "Month": pd.period_range(
                "2026-01",
                periods=3,
                freq="M",
            ),
            "Revenue": [
                100.0,
                120.0,
                150.0,
            ],
        }
    )

    result = calculate_mom_growth(monthly)

    assert pd.isna(result["MoM_Growth"].iloc[0])

    assert result["MoM_Growth"].iloc[1] == pytest.approx(
        20.0
    )

    assert result["MoM_Growth"].iloc[2] == pytest.approx(
        25.0
    )


def test_zero_previous_revenue() -> None:
    monthly = pd.DataFrame(
        {
            "Month": pd.period_range(
                "2026-01",
                periods=2,
                freq="M",
            ),
            "Revenue": [
                0.0,
                100.0,
            ],
        }
    )

    result = calculate_mom_growth(monthly)

    assert pd.isna(result["MoM_Growth"].iloc[0])
    assert pd.isna(result["MoM_Growth"].iloc[1])

def test_invalid_dates_raise_error() -> None:
    dataframe = pd.DataFrame(
        {
            "Order_Date": [
                "2026-01-01",
                "not-a-date",
            ],
            "Order_ID": ["A", "B"],
            "Quantity": [1, 2],
            "Revenue": [100.0, 200.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="Order_Date",
    ):
        calculate_monthly_metrics(dataframe)
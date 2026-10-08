import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.transformation.data_quality import run_quality_checks
from src.analytics.customer_analytics import (
    create_customer_metrics,
    create_monthly_metrics,
    create_return_metrics,
)


def sample_sales_data():
    return pd.DataFrame(
        {
            "invoice": ["10001", "10001", "10002", "10003"],
            "stock_code": ["A", "B", "A", "C"],
            "description": ["Product A", "Product B", "Product A", "Product C"],
            "quantity": [2, 3, 1, 4],
            "invoice_date": pd.to_datetime(
                [
                    "2011-01-05",
                    "2011-01-05",
                    "2011-01-10",
                    "2011-02-15",
                ]
            ),
            "price": [10.0, 5.0, 10.0, 2.5],
            "customer_id": [101.0, 101.0, 102.0, 103.0],
            "country": ["United Kingdom"] * 4,
            "revenue": [20.0, 15.0, 10.0, 10.0],
            "year": [2011, 2011, 2011, 2011],
            "month": [1, 1, 1, 2],
            "day": [5, 5, 10, 15],
            "weekday": ["Wednesday", "Wednesday", "Monday", "Tuesday"],
        }
    )


def sample_returns_data():
    return pd.DataFrame(
        {
            "invoice": ["C100", "C101"],
            "stock_code": ["A", "B"],
            "description": ["Product A", "Product B"],
            "quantity": [-2, -3],
            "invoice_date": pd.to_datetime(
                ["2011-01-10", "2011-02-15"]
            ),
            "price": [10.0, 5.0],
            "customer_id": [101.0, 102.0],
            "country": ["United Kingdom", "Germany"],
        }
    )


def test_data_quality_checks_pass():
    df = sample_sales_data()

    report = run_quality_checks(df)

    assert (report["status"] == "PASS").all()


def test_customer_metrics():
    df = sample_sales_data()

    result = create_customer_metrics(df)

    customer_101 = result[
        result["customer_id"] == 101.0
    ].iloc[0]

    assert customer_101["total_revenue"] == 35.0
    assert customer_101["total_orders"] == 1
    assert customer_101["total_items"] == 5
    assert customer_101["average_order_value"] == 35.0


def test_monthly_metrics():
    df = sample_sales_data()

    result = create_monthly_metrics(df)

    january = result[
        (result["year"] == 2011)
        & (result["month"] == 1)
    ].iloc[0]

    assert january["total_revenue"] == 45.0
    assert january["total_orders"] == 2
    assert january["total_items"] == 6
    assert january["unique_customers"] == 2


def test_return_metrics():
    returns_df = sample_returns_data()

    result = create_return_metrics(returns_df)

    january = result[
        (result["year"] == 2011)
        & (result["month"] == 1)
    ].iloc[0]

    assert january["return_transactions"] == 1
    assert january["returned_items"] == 2
    assert january["return_value"] == 20.0


def test_empty_returns():
    empty_returns = pd.DataFrame(
        columns=[
            "invoice",
            "stock_code",
            "description",
            "quantity",
            "invoice_date",
            "price",
            "customer_id",
            "country",
        ]
    )

    result = create_return_metrics(empty_returns)

    assert result.empty
from pathlib import Path

import pandas as pd


INPUT_FILE = "data/processed/retail_sales_clean.parquet"
RETURNS_FILE = "data/processed/retail_returns.parquet"

OUTPUT_DIR = Path("data/processed/analytics")


def create_customer_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create customer-level revenue and purchasing metrics.
    """

    customer_df = df.dropna(subset=["customer_id"]).copy()

    customer_metrics = (
        customer_df
        .groupby("customer_id")
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("invoice", "nunique"),
            total_items=("quantity", "sum"),
            first_purchase=("invoice_date", "min"),
            last_purchase=("invoice_date", "max")
        )
        .reset_index()
    )

    customer_metrics["average_order_value"] = (
        customer_metrics["total_revenue"]
        / customer_metrics["total_orders"]
    )

    customer_metrics["customer_lifetime_days"] = (
        customer_metrics["last_purchase"]
        - customer_metrics["first_purchase"]
    ).dt.days

    customer_metrics = customer_metrics.sort_values(
        "total_revenue",
        ascending=False
    )

    return customer_metrics


def create_monthly_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create monthly business performance metrics.
    """

    monthly_metrics = (
        df
        .groupby(["year", "month"])
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("invoice", "nunique"),
            total_items=("quantity", "sum"),
            unique_customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    monthly_metrics["average_order_value"] = (
        monthly_metrics["total_revenue"]
        / monthly_metrics["total_orders"]
    )

    monthly_metrics = monthly_metrics.sort_values(
        ["year", "month"]
    )

    return monthly_metrics


def create_return_metrics(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze returned/cancelled transactions.
    """

    if returns_df.empty:
        return pd.DataFrame(
            columns=[
                "year",
                "month",
                "return_transactions",
                "returned_items",
                "return_value"
            ]
        )

    returns_df = returns_df.copy()

    returns_df["return_value"] = (
        returns_df["quantity"].abs()
        * returns_df["price"]
    )

    returns_df["year"] = returns_df["invoice_date"].dt.year
    returns_df["month"] = returns_df["invoice_date"].dt.month

    return_metrics = (
        returns_df
        .groupby(["year", "month"])
        .agg(
            return_transactions=("invoice", "nunique"),
            returned_items=("quantity", lambda x: x.abs().sum()),
            return_value=("return_value", "sum")
        )
        .reset_index()
        .sort_values(["year", "month"])
    )

    return return_metrics


def main():

    print("=" * 70)
    print("BUSINESS ANALYTICS")
    print("=" * 70)

    print("\nLoading sales data...")

    df = pd.read_parquet(INPUT_FILE)

    print(f"Sales rows: {len(df):,}")

    print("\nLoading returns data...")

    returns_df = pd.read_parquet(RETURNS_FILE)

    print(f"Return rows: {len(returns_df):,}")

    # ---------------------------------------------------------
    # CUSTOMER ANALYTICS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("CUSTOMER ANALYTICS")
    print("=" * 70)

    customer_metrics = create_customer_metrics(df)

    print("\nTop 10 customers by revenue:")

    print(
        customer_metrics[
            [
                "customer_id",
                "total_revenue",
                "total_orders",
                "total_items",
                "average_order_value"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # MONTHLY ANALYTICS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("MONTHLY ANALYTICS")
    print("=" * 70)

    monthly_metrics = create_monthly_metrics(df)

    print("\nMonthly performance:")

    print(
        monthly_metrics.tail(12).to_string(index=False)
    )

    # ---------------------------------------------------------
    # RETURN ANALYTICS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("RETURN ANALYTICS")
    print("=" * 70)

    return_metrics = create_return_metrics(returns_df)

    print("\nReturn/cancellation metrics:")

    print(
        return_metrics.tail(12).to_string(index=False)
    )

    # ---------------------------------------------------------
    # SAVE OUTPUTS
    # ---------------------------------------------------------

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    customer_output = OUTPUT_DIR / "customer_metrics.parquet"
    monthly_output = OUTPUT_DIR / "monthly_metrics.parquet"
    return_output = OUTPUT_DIR / "return_metrics.parquet"

    customer_metrics.to_parquet(
        customer_output,
        engine="pyarrow",
        index=False
    )

    monthly_metrics.to_parquet(
        monthly_output,
        engine="pyarrow",
        index=False
    )

    return_metrics.to_parquet(
        return_output,
        engine="pyarrow",
        index=False
    )

    print("\n" + "=" * 70)
    print("ANALYTICS OUTPUTS SAVED")
    print("=" * 70)

    print(customer_output)
    print(monthly_output)
    print(return_output)


if __name__ == "__main__":
    main()
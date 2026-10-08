import pandas as pd
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = "data/raw/online+retail+ii/online_retail_II.xlsx"

OUTPUT_DIR = Path("data/processed")

CLEAN_FILE = OUTPUT_DIR / "retail_sales_clean.parquet"
RETURNS_FILE = OUTPUT_DIR / "retail_returns.parquet"


# ============================================================
# Load Raw Data
# ============================================================

def load_data() -> pd.DataFrame:
    """Load both yearly sheets and combine them."""

    sheets = [
        "Year 2009-2010",
        "Year 2010-2011"
    ]

    frames = []

    for sheet in sheets:
        print(f"Reading: {sheet}")

        df = pd.read_excel(
            INPUT_FILE,
            sheet_name=sheet
        )

        frames.append(df)

    combined_df = pd.concat(
        frames,
        ignore_index=True
    )

    print(f"\nCombined rows: {len(combined_df):,}")

    return combined_df


# ============================================================
# Clean and Transform
# ============================================================

def clean_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:

    print("\n--- Cleaning Data ---")

    original_rows = len(df)

    # Remove exact duplicates
    duplicate_count = df.duplicated().sum()

    df = df.drop_duplicates().copy()

    print(
        f"Duplicates removed: {duplicate_count:,}"
    )

    # Standardize column names
    df.columns = [
        "invoice",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "price",
        "customer_id",
        "country"
    ]

    # Standardize data types
    df["invoice"] = df["invoice"].astype(str)

    df["stock_code"] = df["stock_code"].astype(str)

    df["description"] = df["description"].astype("string")

    df["country"] = df["country"].astype("string")

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Convert timestamp precision to microseconds.
    # This keeps the Parquet file compatible with PySpark.
    # --------------------------------------------------------

    df["invoice_date"] = (
        df["invoice_date"]
        .astype("datetime64[us]")
    )

    # Separate returns/cancellations
    returns_df = df[
        df["quantity"] <= 0
    ].copy()

    print(
        f"Return/cancellation rows: {len(returns_df):,}"
    )

    # Keep positive sales
    sales_df = df[
        df["quantity"] > 0
    ].copy()

    # Remove invalid prices
    invalid_price_count = (
        sales_df["price"] <= 0
    ).sum()

    sales_df = sales_df[
        sales_df["price"] > 0
    ].copy()

    print(
        f"Invalid-price rows removed: "
        f"{invalid_price_count:,}"
    )

    # Calculate revenue
    sales_df["revenue"] = (
        sales_df["quantity"] *
        sales_df["price"]
    )

    # Date attributes
    sales_df["year"] = (
        sales_df["invoice_date"].dt.year
    )

    sales_df["month"] = (
        sales_df["invoice_date"].dt.month
    )

    sales_df["day"] = (
        sales_df["invoice_date"].dt.day
    )

    sales_df["weekday"] = (
        sales_df["invoice_date"].dt.day_name()
    )

    # Sort
    sales_df = sales_df.sort_values(
        by="invoice_date"
    ).reset_index(drop=True)

    returns_df = returns_df.sort_values(
        by="invoice_date"
    ).reset_index(drop=True)

    # Cleaning summary
    print("\n--- Cleaning Summary ---")

    print(
        f"Original rows: {original_rows:,}"
    )

    print(
        f"Clean sales rows: {len(sales_df):,}"
    )

    print(
        f"Return rows: {len(returns_df):,}"
    )

    print(
        f"Total revenue: "
        f"£{sales_df['revenue'].sum():,.2f}"
    )

    return sales_df, returns_df


# ============================================================
# Save Processed Data
# ============================================================

def save_data(
    sales_df: pd.DataFrame,
    returns_df: pd.DataFrame
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    sales_df.to_parquet(
        CLEAN_FILE,
        index=False
    )

    returns_df.to_parquet(
        RETURNS_FILE,
        index=False
    )

    print("\n--- Files Saved ---")

    print(
        f"Sales: {CLEAN_FILE}"
    )

    print(
        f"Returns: {RETURNS_FILE}"
    )


# ============================================================
# Main
# ============================================================

def main():

    df = load_data()

    sales_df, returns_df = clean_data(df)

    save_data(
        sales_df,
        returns_df
    )


if __name__ == "__main__":
    main()
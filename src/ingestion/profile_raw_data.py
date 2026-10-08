import pandas as pd

FILE_PATH = "data/raw/online+retail+ii/online_retail_II.xlsx"


def profile_sheet(sheet_name: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"SHEET: {sheet_name}")
    print(f"{'=' * 60}")

    df = pd.read_excel(FILE_PATH, sheet_name=sheet_name)

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\n--- Data Quality Checks ---")

    print(f"Duplicate rows: {df.duplicated().sum():,}")

    print(f"Missing Customer ID: {df['Customer ID'].isna().sum():,}")

    print(f"Missing Description: {df['Description'].isna().sum():,}")

    print(f"Quantity <= 0: {(df['Quantity'] <= 0).sum():,}")

    print(f"Price <= 0: {(df['Price'] <= 0).sum():,}")

    print(f"Unique invoices: {df['Invoice'].nunique():,}")

    print(f"Unique products: {df['StockCode'].nunique():,}")

    print(f"Unique customers: {df['Customer ID'].nunique():,}")

    print(f"Unique countries: {df['Country'].nunique():,}")

    print(f"Date range: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")

    print("\nTop 10 countries:")
    print(df["Country"].value_counts().head(10))

    print("\nSample records:")
    print(df.head(5).to_string(index=False))


def main() -> None:
    excel_file = pd.ExcelFile(FILE_PATH)

    print("Available Sheets:")
    for sheet in excel_file.sheet_names:
        print(f"  - {sheet}")

    for sheet in excel_file.sheet_names:
        profile_sheet(sheet)


if __name__ == "__main__":
    main()
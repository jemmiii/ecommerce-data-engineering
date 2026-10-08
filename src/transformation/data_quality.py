from pathlib import Path

import pandas as pd


INPUT_FILE = "data/processed/retail_sales_clean.parquet"
REPORT_FILE = Path("data/processed/data_quality_report.csv")


def run_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    checks = []

    # 1. Record count
    checks.append({
        "check": "Record count",
        "status": "PASS" if len(df) > 0 else "FAIL",
        "value": len(df),
        "details": "Clean sales dataset contains records."
    })

    # 2. Duplicate rows
    duplicates = int(df.duplicated().sum())

    checks.append({
        "check": "Duplicate rows",
        "status": "PASS" if duplicates == 0 else "FAIL",
        "value": duplicates,
        "details": "Clean dataset should not contain exact duplicates."
    })

    # 3. Missing invoice
    missing_invoice = int(df["invoice"].isna().sum())

    checks.append({
        "check": "Missing invoice",
        "status": "PASS" if missing_invoice == 0 else "FAIL",
        "value": missing_invoice,
        "details": "Every sales record should have an invoice."
    })

    # 4. Missing stock code
    missing_stock_code = int(df["stock_code"].isna().sum())

    checks.append({
        "check": "Missing stock code",
        "status": "PASS" if missing_stock_code == 0 else "FAIL",
        "value": missing_stock_code,
        "details": "Every sales record should have a product code."
    })

    # 5. Invalid quantity
    invalid_quantity = int((df["quantity"] <= 0).sum())

    checks.append({
        "check": "Invalid quantity",
        "status": "PASS" if invalid_quantity == 0 else "FAIL",
        "value": invalid_quantity,
        "details": "Clean sales data should contain only positive quantities."
    })

    # 6. Invalid price
    invalid_price = int((df["price"] <= 0).sum())

    checks.append({
        "check": "Invalid price",
        "status": "PASS" if invalid_price == 0 else "FAIL",
        "value": invalid_price,
        "details": "Clean sales data should contain positive prices."
    })

    # 7. Missing invoice date
    missing_date = int(df["invoice_date"].isna().sum())

    checks.append({
        "check": "Missing invoice date",
        "status": "PASS" if missing_date == 0 else "FAIL",
        "value": missing_date,
        "details": "Every sales record should have an invoice date."
    })

    # 8. Revenue validation
    calculated_revenue = df["quantity"] * df["price"]

    revenue_mismatch = int(
        (abs(df["revenue"] - calculated_revenue) > 0.01).sum()
    )

    checks.append({
        "check": "Revenue calculation",
        "status": "PASS" if revenue_mismatch == 0 else "FAIL",
        "value": revenue_mismatch,
        "details": "Revenue should equal quantity multiplied by price."
    })

    return pd.DataFrame(checks)


def main():

    print("=" * 70)
    print("DATA QUALITY VALIDATION")
    print("=" * 70)

    print("\nLoading cleaned dataset...")

    df = pd.read_parquet(INPUT_FILE)

    print(f"Rows loaded: {len(df):,}")

    report = run_quality_checks(df)

    print("\nQuality Check Results:")
    print("-" * 70)

    print(
        report[
            ["check", "status", "value", "details"]
        ].to_string(index=False)
    )

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    report.to_csv(REPORT_FILE, index=False)

    print("\nQuality report saved:")
    print(REPORT_FILE)

    failed_checks = int((report["status"] == "FAIL").sum())

    print("\n" + "=" * 70)

    if failed_checks == 0:
        print("ALL DATA QUALITY CHECKS PASSED")
    else:
        print(f"DATA QUALITY CHECKS FAILED: {failed_checks}")

    print("=" * 70)


if __name__ == "__main__":
    main()
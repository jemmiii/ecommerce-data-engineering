from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    countDistinct,
    round
)

INPUT_FILE = "data/processed/retail_sales_clean.parquet"
OUTPUT_DIR = Path("data/processed/spark")


def create_spark_session():
    """Create local Spark session."""

    spark = (
        SparkSession.builder
        .appName("ECommerceDataEngineering")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark


def load_data(spark):
    """Load cleaned retail sales data."""

    print("\nLoading cleaned sales data...")

    df = spark.read.parquet(INPUT_FILE)

    print(f"Rows loaded: {df.count():,}")

    print("\nSchema:")
    df.printSchema()

    return df


def create_monthly_sales(df):
    """Calculate monthly revenue."""

    monthly_sales = (
        df.groupBy("year", "month")
        .agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            countDistinct("invoice").alias("unique_invoices"),
            countDistinct("customer_id").alias("unique_customers")
        )
        .orderBy("year", "month")
    )

    return monthly_sales


def create_country_sales(df):
    """Calculate sales by country."""

    country_sales = (
        df.groupBy("country")
        .agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            countDistinct("invoice").alias("unique_invoices"),
            countDistinct("customer_id").alias("unique_customers")
        )
        .orderBy(col("total_revenue").desc())
    )

    return country_sales


def create_product_sales(df):
    """Calculate sales by product."""

    product_sales = (
        df.groupBy("stock_code", "description")
        .agg(
            round(sum("revenue"), 2).alias("total_revenue"),
            col("stock_code").alias("product_code"),
            countDistinct("invoice").alias("unique_invoices")
        )
        .orderBy(col("total_revenue").desc())
    )

    return product_sales


def save_spark_result_as_parquet(df, output_path):
    """
    Convert the small aggregated Spark DataFrame to Pandas
    and save it using PyArrow.

    This avoids the Windows Hadoop/winutils filesystem issue.
    """

    pandas_df = df.toPandas()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    pandas_df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False
    )

    print(f"Saved: {output_path}")


def main():

    print("=" * 70)
    print("E-COMMERCE DATA ENGINEERING - SPARK ETL")
    print("=" * 70)

    spark = create_spark_session()

    try:

        # ---------------------------------------------------------
        # 1. LOAD DATA
        # ---------------------------------------------------------

        df = load_data(spark)

        # ---------------------------------------------------------
        # 2. MONTHLY SALES
        # ---------------------------------------------------------

        print("\n" + "=" * 70)
        print("MONTHLY SALES")
        print("=" * 70)

        monthly_sales = create_monthly_sales(df)

        monthly_sales.show(20, truncate=False)

        # ---------------------------------------------------------
        # 3. COUNTRY SALES
        # ---------------------------------------------------------

        print("\n" + "=" * 70)
        print("COUNTRY SALES")
        print("=" * 70)

        country_sales = create_country_sales(df)

        country_sales.show(10, truncate=False)

        # ---------------------------------------------------------
        # 4. PRODUCT SALES
        # ---------------------------------------------------------

        print("\n" + "=" * 70)
        print("TOP PRODUCTS")
        print("=" * 70)

        product_sales = create_product_sales(df)

        product_sales.show(10, truncate=False)

        # ---------------------------------------------------------
        # 5. SAVE RESULTS
        # ---------------------------------------------------------

        print("\n" + "=" * 70)
        print("SAVING RESULTS")
        print("=" * 70)

        save_spark_result_as_parquet(
            monthly_sales,
            OUTPUT_DIR / "monthly_sales.parquet"
        )

        save_spark_result_as_parquet(
            country_sales,
            OUTPUT_DIR / "country_sales.parquet"
        )

        save_spark_result_as_parquet(
            product_sales,
            OUTPUT_DIR / "product_sales.parquet"
        )

        print("\n" + "=" * 70)
        print("SPARK ETL COMPLETED SUCCESSFULLY")
        print("=" * 70)

    finally:

        spark.stop()


if __name__ == "__main__":
    main()
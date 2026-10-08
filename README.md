# E-Commerce Data Engineering Pipeline

An end-to-end data engineering pipeline built using Python, PySpark, Pandas, and Parquet to process and analyze the UCI Online Retail II dataset.

## Project Overview

This project processes more than 1 million retail transaction records through a structured data engineering workflow.

The pipeline performs:

- Raw data profiling
- Data cleaning and transformation
- Returns and cancellation handling
- Parquet-based data storage
- PySpark ETL processing
- Data quality validation
- Customer-level analytics
- Monthly business analytics
- Product and country-level analysis
- Automated pipeline tests
- Airflow DAG definition for pipeline orchestration

## Architecture

```text
UCI Online Retail II Dataset
            |
            v
      Raw Excel Data
            |
            v
      Data Profiling
            |
            v
    Data Cleaning Layer
            |
      +-----+-----+
      |           |
      v           v
Clean Sales   Returns Data
      |
      v
 Parquet Data Layer
      |
      v
    PySpark ETL
      |
 +----+---------+---------+
 |              |         |
 v              v         v
Monthly       Country   Product
Sales         Sales     Sales
      |
      v
Data Quality Checks
      |
      v
Business Analytics
      |
 +----+---------+---------+
 |              |         |
 v              v         v
Customer      Monthly   Returns
Metrics       Metrics   Metrics

Dataset
The project uses the UCI Online Retail II dataset.
The dataset contains online retail transaction records with information such as:
- Invoice
- Stock Code
- Product Description
- Quantity
- Invoice Date
- Price
- Customer ID
- Country
The raw dataset contains more than 1 million transaction records across two time periods.
Data Processing
1. Data Profiling
The raw dataset is profiled before transformation to identify:
- Missing values
- Duplicate records
- Invalid quantities
- Invalid prices
- Unique invoices
- Unique products
- Unique customers
- Country distribution
- Date range
2. Data Cleaning
The cleaning pipeline:
- Combines both dataset sheets
- Removes exact duplicate records
- Separates return/cancellation transactions
- Removes invalid-price records
- Keeps valid positive-quantity sales
- Calculates transaction revenue
- Adds year, month, day, and weekday attributes
- Stores cleaned data in Parquet format
The resulting clean sales dataset contains:
1,007,914 valid sales records
A separate dataset containing 22,496 return/cancellation records is also maintained for analysis.
3. PySpark ETL
PySpark is used to process and aggregate the cleaned transaction data.
The ETL pipeline generates:
- Monthly sales
- Country-level sales
- Product-level sales
The aggregated outputs are stored in Parquet format.
4. Data Quality Validation
Automated data quality checks validate:
- Record count
- Duplicate records
- Missing invoice IDs
- Missing stock codes
- Invalid quantities
- Invalid prices
- Missing invoice dates
- Revenue calculation consistency
Current validation result:
8/8 data quality checks passed
5. Business Analytics
The analytics layer generates:
Customer Metrics
- Total revenue
- Total orders
- Total items
- Average order value
- First purchase date
- Last purchase date
- Customer lifetime duration
Monthly Metrics
- Total revenue
- Total orders
- Total items
- Unique customers
- Average order value
Return Metrics
- Return transactions
- Returned items
- Return value
Key Results
The pipeline successfully processed:
- 1,007,914 clean sales records
- 22,496 return/cancellation records
- 8/8 data quality checks passed
- 5/5 automated tests passed
The pipeline produces analytical outputs for:
- Monthly revenue trends
- Country performance
- Product performance
- Customer revenue
- Average order value
- Return/cancellation trends
Technology Stack
Programming
- Python 3.11
Data Engineering
- PySpark 3.5.6
- Pandas 2.2.3
- PyArrow 18.1.0
- Parquet
Data Quality & Testing
- Pytest
Orchestration
- Apache Airflow DAG definition
Development Tools
- VS Code
- Git
- GitHub
Project Structure
ecommerce-data-engineering/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── ingestion/
│   │   └── profile_raw_data.py
│   │
│   ├── transformation/
│   │   ├── clean_retail_data.py
│   │   ├── spark_etl.py
│   │   ├── data_quality.py
│   │   └── __init__.py
│   │
│   └── analytics/
│       ├── customer_analytics.py
│       └── __init__.py
│
├── dags/
│   └── ecommerce_pipeline.py
│
├── tests/
│   └── test_pipeline.py
│
├── notebooks/
├── sql/
│
├── requirements.txt
└── README.md

Installation
Clone the repository:
git clone https://github.com/jemmiii/ecommerce-data-engineering.git
cd ecommerce-data-engineering

Create a virtual environment:
python -m venv venv

Activate the environment on Windows:
venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

Running the Pipeline
Data Profiling
python src/ingestion/profile_raw_data.py

Data Cleaning
python src/transformation/clean_retail_data.py

PySpark ETL
python src/transformation/spark_etl.py

Data Quality Checks
python src/transformation/data_quality.py

Business Analytics
python src/analytics/customer_analytics.py

Run Tests
pytest -v

Expected result:
5 passed

Data Outputs
The pipeline generates processed data under:
data/processed/

Major outputs include:
retail_sales_clean.parquet
retail_returns.parquet

spark/
├── monthly_sales.parquet
├── country_sales.parquet
└── product_sales.parquet

analytics/
├── customer_metrics.parquet
├── monthly_metrics.parquet
└── return_metrics.parquet

data_quality_report.csv

Orchestration
An Apache Airflow DAG is included to define the pipeline task dependencies:
Clean Data
    ↓
Spark ETL
    ↓
Data Quality Checks
    ↓
Business Analytics

The current project includes the DAG definition. Production Airflow deployment is a future enhancement.
Engineering Practices
This project demonstrates:
- ETL pipeline design
- Data cleaning and transformation
- Distributed data processing with PySpark
- Columnar storage using Parquet
- Data quality validation
- Business-oriented analytics
- Automated testing
- Pipeline orchestration design
Future Improvements
Potential extensions include:
- AWS S3 data lake integration
- AWS EMR or AWS Glue
- Production Airflow deployment
- Incremental data processing
- Partitioned Parquet datasets
- Spark SQL analytics
- Data warehouse integration
- Pipeline monitoring and observability
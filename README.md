# E-Commerce Data Engineering Pipeline

An end-to-end data engineering pipeline built with **Python, PySpark, Pandas, Parquet, and Pytest** to process and analyze the **UCI Online Retail II** dataset containing more than 1 million retail transaction records.

---

## 🚀 Project Overview

This project demonstrates a complete data engineering workflow from raw data profiling and cleaning to scalable ETL processing, data quality validation, and business analytics.

### Key Capabilities

- Raw retail data profiling
- Data cleaning and transformation
- Duplicate and invalid transaction handling
- Returns and cancellation separation
- Parquet-based data storage
- PySpark ETL and aggregations
- Automated data quality validation
- Customer-level analytics
- Monthly business analytics
- Product and country-level analysis
- Automated unit tests
- Apache Airflow DAG definition

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[UCI Online Retail II Dataset] --> B[Raw Excel Data]
    B --> C[Data Profiling]
    C --> D[Data Cleaning & Transformation]

    D --> E[Clean Sales Data]
    D --> F[Returns & Cancellations]

    E --> G[Parquet Data Layer]
    G --> H[PySpark ETL]

    H --> I[Monthly Sales]
    H --> J[Country Sales]
    H --> K[Product Sales]

    G --> L[Data Quality Validation]

    E --> M[Business Analytics]
    F --> M

    M --> N[Customer Metrics]
    M --> O[Monthly Metrics]
    M --> P[Return Metrics]
📊 Dataset
The project uses the UCI Online Retail II dataset.
The dataset contains online retail transaction information including:
Column	Description
Invoice	Invoice/transaction identifier
StockCode	Product identifier
Description	Product description
Quantity	Number of units purchased
InvoiceDate	Transaction date and time
Price	Unit price
Customer ID	Customer identifier
Country	Customer country


The dataset contains transaction records covering 2009–2011.
🔄 Data Pipeline
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
- Transaction date range
2. Data Cleaning
The cleaning pipeline performs the following operations:
- Combines both dataset sheets
- Removes exact duplicate records
- Separates return/cancellation transactions
- Removes invalid-price records
- Keeps valid positive-quantity sales
- Calculates transaction revenue
- Adds year, month, day, and weekday attributes
- Stores cleaned data in Parquet format
Cleaned Dataset
Metric	Result
Clean sales records	1,007,914
Return/cancellation records	22,496
Total revenue	£20.48M


3. PySpark ETL
PySpark is used to process and aggregate the cleaned transaction dataset.
The ETL pipeline generates:
- Monthly sales
- Country-level sales
- Product-level sales
The aggregated results are stored as Parquet files.
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
Validation Result
8 / 8 data quality checks passed ✅
5. Business Analytics
The analytics layer generates customer, monthly, and return-related metrics.
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
📈 Key Results
The completed pipeline successfully produced:
Result	Value
Clean sales records	1,007,914
Return/cancellation records	22,496
Data quality checks	8 / 8 passed
Automated tests	5 / 5 passed
Clean sales dataset	Parquet
Analytics outputs	Parquet


The pipeline provides analytical outputs for:
- Monthly revenue trends
- Country performance
- Product performance
- Customer revenue
- Average order value
- Return and cancellation trends
🧪 Testing
The project includes automated tests using Pytest.
The test suite validates:
- Data quality checks
- Customer metric calculations
- Monthly metric calculations
- Return metric calculations
- Empty return-data handling
Test Result
5 passed

Run the tests with:
pytest -v

⚙️ Technology Stack
Category	Technologies
Language	Python 3.11
Data Processing	PySpark 3.5.6
Data Analysis	Pandas 2.2.3
Storage	Apache Parquet / PyArrow
Testing	Pytest
Orchestration	Apache Airflow DAG
Development	VS Code
Version Control	Git / GitHub


📁 Project Structure
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
├── .gitignore
└── README.md

🛠️ Installation
Clone the repository
git clone https://github.com/jemmiii/ecommerce-data-engineering.git
cd ecommerce-data-engineering

Create a virtual environment
python -m venv venv

Activate the environment
Windows
venv\Scripts\Activate.ps1

Install dependencies
pip install -r requirements.txt

▶️ Running the Pipeline
1. Profile raw data
python src/ingestion/profile_raw_data.py

2. Clean the dataset
python src/transformation/clean_retail_data.py

3. Run PySpark ETL
python src/transformation/spark_etl.py

4. Run data quality checks
python src/transformation/data_quality.py

5. Run business analytics
python src/analytics/customer_analytics.py

6. Run automated tests
pytest -v

📦 Generated Outputs
The pipeline generates the following processed datasets:
data/processed/
│
├── retail_sales_clean.parquet
├── retail_returns.parquet
├── data_quality_report.csv
│
├── spark/
│   ├── monthly_sales.parquet
│   ├── country_sales.parquet
│   └── product_sales.parquet
│
└── analytics/
    ├── customer_metrics.parquet
    ├── monthly_metrics.parquet
    └── return_metrics.parquet

🔄 Pipeline Orchestration
An Apache Airflow DAG is included to define the dependency between the major pipeline tasks.
Clean Data
    ↓
Spark ETL
    ↓
Data Quality Checks
    ↓
Business Analytics

The current repository contains the Airflow DAG definition. A production Airflow deployment is planned as a future enhancement.
💡 Engineering Practices Demonstrated
This project demonstrates practical data engineering concepts including:
- ETL pipeline design
- Data profiling
- Data cleaning and transformation
- Distributed data processing with PySpark
- Columnar storage using Parquet
- Data quality validation
- Business-oriented analytics
- Automated testing
- Pipeline orchestration design
- Git-based version control
🔮 Future Improvements
Potential future enhancements include:
- AWS S3 data lake integration
- AWS EMR or AWS Glue processing
- Production Airflow deployment
- Incremental data processing
- Partitioned Parquet datasets
- Spark SQL analytics
- Data warehouse integration
- Pipeline monitoring and observability
👨‍💻 Author
Jemin Patidar
B.Tech Information Technology
Manipal University Jaipur
- GitHub: https://github.com/jemmiii
- Portfolio: https://jeminpatidar-portfolio.vercel.app/

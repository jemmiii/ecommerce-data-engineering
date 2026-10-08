from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = r"C:\Users\JEMIN\OneDrive\Desktop\ecommerce-data-engineering"

PYTHON = rf"{PROJECT_DIR}\venv\Scripts\python.exe"


with DAG(
    dag_id="ecommerce_data_pipeline",
    description="End-to-end e-commerce data engineering pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "data-engineering", "pyspark"],
) as dag:

    clean_data = BashOperator(
        task_id="clean_retail_data",
        bash_command=(
            f'cd /d "{PROJECT_DIR}" && '
            f'"{PYTHON}" src/transformation/clean_retail_data.py'
        ),
    )

    spark_etl = BashOperator(
        task_id="spark_etl",
        bash_command=(
            f'cd /d "{PROJECT_DIR}" && '
            f'"{PYTHON}" src/transformation/spark_etl.py'
        ),
    )

    data_quality = BashOperator(
        task_id="data_quality_checks",
        bash_command=(
            f'cd /d "{PROJECT_DIR}" && '
            f'"{PYTHON}" src/transformation/data_quality.py'
        ),
    )

    business_analytics = BashOperator(
        task_id="business_analytics",
        bash_command=(
            f'cd /d "{PROJECT_DIR}" && '
            f'"{PYTHON}" src/analytics/customer_analytics.py'
        ),
    )

    clean_data >> spark_etl >> data_quality >> business_analytics
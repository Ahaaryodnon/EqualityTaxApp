"""Airflow DAG for ingesting UK MPs' financial interests data."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "uk_mps_financial_interests",
    default_args=default_args,
    description="Ingest and process UK MPs' financial interests data",
    schedule_interval="0 2 * * 1",  # Every Monday at 2 AM
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["ingest", "uk", "politicians", "financial_interests"],
)


# Task to run the Scrapy spider
run_spider = BashOperator(
    task_id="run_uk_register_spider",
    bash_command=(
        "mkdir -p /tmp/uk_mps && "
        "cd /app/services/ingestion && "
        "scrapy crawl uk_register_of_interests "
        "-o /tmp/uk_mps/register_of_interests_{{ ds }}.json"
    ),
    dag=dag,
)


# Task to run data quality checks
def check_data_quality(**kwargs):
    """Check the quality of the scraped data.

    Args:
        **kwargs: Airflow context variables

    Returns:
        bool: True if data quality checks pass
    """
    import json
    import os

    ds = kwargs["ds"]
    file_path = f"/tmp/uk_mps/register_of_interests_{ds}.json"

    if not os.path.exists(file_path):
        raise Exception(f"Scraped data file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise Exception(f"Failed to read scraped data: {e}")

    # Perform data quality checks
    person_items = [item for item in data if "full_name" in item]
    interest_items = [item for item in data if "person_name" in item and "type" in item]

    # Check if we have at least some MPs and interests
    if len(person_items) < 10:
        raise Exception(f"Too few MPs found: {len(person_items)}")

    if len(interest_items) < 50:
        raise Exception(f"Too few interests found: {len(interest_items)}")

    # Check for required fields in person items
    for item in person_items:
        if not item.get("full_name") or not item.get("parliament_id"):
            raise Exception(f"Missing required fields in person item: {item}")

    # Check for required fields in interest items
    for item in interest_items:
        if not item.get("person_name") or not item.get("type"):
            raise Exception(f"Missing required fields in interest item: {item}")

    return True


check_data = PythonOperator(
    task_id="check_data_quality",
    python_callable=check_data_quality,
    provide_context=True,
    dag=dag,
)


# Task to run SQL transformation
transform_sql = PostgresOperator(
    task_id="transform_data",
    postgres_conn_id="inequality_db",
    sql="sql/transform/uk_mps_financial_interests.sql",
    params={"ds": "{{ ds }}"},
    dag=dag,
)


# Set up the task dependencies
run_spider >> check_data >> transform_sql 
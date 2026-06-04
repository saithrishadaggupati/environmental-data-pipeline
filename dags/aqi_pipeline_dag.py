from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "sai_thrisha",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}

with DAG(
    dag_id="aqi_pipeline",
    default_args=default_args,
    description="Fetch AQI data for 101 Indian cities, store to MongoDB, and export CSV",
    schedule="0 */6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["aqi", "data-engineering"],
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_aqi_data",
        python_callable=lambda: __import__(
            "src.ingestion.fetch_aqi", fromlist=["fetch_all_cities"]
        ).fetch_all_cities(),
    )

    store_mongo_task = PythonOperator(
        task_id="store_to_mongodb",
        python_callable=lambda: __import__(
            "src.loading.mongo_store", fromlist=["store_raw_to_mongo"]
        ).store_raw_to_mongo(),
    )

    clean_task = PythonOperator(
        task_id="clean_aqi_data",
        python_callable=lambda: __import__(
            "src.transformation.clean_aqi", fromlist=["clean_data"]
        ).clean_data(),
    )

    fetch_task >> store_mongo_task >> clean_task
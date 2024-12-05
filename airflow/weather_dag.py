from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from tasks.fetch_weather import fetch
from tasks.store_weather import store

# Definisikan DAG untuk Airflow
default_args = {
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 12, 4),
}

dag = DAG(
    "weather_dag",
    default_args=default_args,
    description="Fetch and store weather data for cities",
    schedule_interval=timedelta(hours=1),
    catchup=False,
)

start_task = EmptyOperator(task_id="start_task", dag=dag)

fetch_task = PythonOperator(task_id="fetch_weather", python_callable=fetch, dag=dag)
store_task = PythonOperator(task_id="store_weather", python_callable=store, dag=dag)

end_task = EmptyOperator(task_id="end_task", dag=dag)

start_task >> fetch_task >> store_task >> end_task
from airflow import DAG
from airflow.operators.python import PythonOperator  # Perbarui modul ini
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def update_weather_data():
    # Simulasi pembaruan data cuaca
    new_data = {
        "temperature": [301.15],
        "pressure": [1009],
        "humidity": [80],
        "wind_speed": [3.2],
        "weather": ["Rain"],
    }
    df = pd.DataFrame(new_data)
    df.to_csv("/opt/airflow/data/weather_data.csv", index=False)

with DAG(
    "weather_monitoring_dag",
    default_args=default_args,
    description="DAG for Weather Monitoring",
    schedule="0 * * * *",  # Ganti schedule_interval dengan schedule
    start_date=datetime(2023, 12, 1),
    catchup=False,
) as dag:
    update_weather = PythonOperator(
        task_id="update_weather_data",
        python_callable=update_weather_data,
    )

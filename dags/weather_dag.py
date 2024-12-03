from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

# Fungsi untuk mengambil data cuaca
def fetch_weather_data():
    api_key = "4c4567a6b7573ad25f40c085e0ebf302"  # Ganti dengan API Key Anda
    city = "Surabaya"  # Ganti dengan kota Anda
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        print(f"Weather in {city}: {weather}")
    else:
        print("Failed to fetch weather data")

# Konfigurasi DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='weather_monitoring',
    default_args=default_args,
    description='A DAG to fetch weather data hourly',
    schedule_interval='@hourly',
    start_date=datetime(2024, 12, 1),
    catchup=False,
)

fetch_weather_task = PythonOperator(
    task_id='fetch_weather',
    python_callable=fetch_weather_data,
    dag=dag,
)

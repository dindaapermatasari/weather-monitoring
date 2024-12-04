from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import requests
import logging

# Konfigurasi PostgreSQL
DB_CONFIG = {
    'dbname': 'weather_data',
    'user': 'postgres',  # Ganti dengan username PostgreSQL Anda
    'password': '123456',  # Ganti dengan password PostgreSQL Anda
    'host': 'localhost',
    'port': 5432
}

# API Key untuk OpenWeatherMap
API_KEY = '4c4567a6b7573ad25f40c085e0ebf302'  # Ganti dengan API Key Anda

def get_db_connection():
    """Fungsi untuk menghubungkan ke database PostgreSQL"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def get_weather_data(city):
    """Fungsi untuk mengambil data cuaca dari API OpenWeatherMap"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["description"]
        }
        return weather
    return None

def fetch_and_store_weather_data():
    """Fungsi untuk mengambil data cuaca dari API dan menyimpannya ke database"""
    try:
        # Ambil daftar kota dari database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT city FROM weather_history;")  # Ambil semua kota unik
        cities = cursor.fetchall()
        
        for city_tuple in cities:
            city = city_tuple[0]
            weather_data = get_weather_data(city)
            
            if weather_data:
                # Simpan data cuaca ke database PostgreSQL
                cursor.execute('''
                    INSERT INTO weather_history (city, temperature, pressure, humidity, wind_speed, weather, timestamp) 
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ''', (city, weather_data["temperature"], weather_data["pressure"],
                      weather_data["humidity"], weather_data["wind_speed"],
                      weather_data["weather"]))
                conn.commit()
            else:
                logging.error(f"Failed to fetch weather data for city: {city}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error fetching and storing weather data: {str(e)}")

# Definisikan DAG untuk Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 12, 4),
}

dag = DAG(
    'weather_dag',
    default_args=default_args,
    description='Fetch and store weather data for cities',
    schedule_interval=timedelta(hours=1),  # Menjalankan setiap jam
    catchup=False,
)

# Task untuk fetch dan store data cuaca
fetch_weather_task = PythonOperator(
    task_id='fetch_and_store_weather_data',
    python_callable=fetch_and_store_weather_data,
    dag=dag,
)

import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv('API_KEY')

DB_CONFIG = {
    'dbname': 'weather_data',
    'user': 'postgres',  
    'password': 'postgres',  
    'host': 'postgres',  
    'port': 5432
}

def fetch():
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    cities = ["Batu", "Blitar", "Kediri", "Madiun", "Malang", "Mojokerto", "Pasuruan", "Probolinggo", "Surabaya"]
    results = []
    
    for city in cities:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "pressure": data["main"]["pressure"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "weather": data["weather"][0]["description"],
            }
            results.append(weather_data)
            print(f"Data cuaca berhasil didapatkan untuk kota: {city}")
        else:
            print(f"Gagal mendapatkan data untuk kota: {city}. HTTP Status Code: {response.status_code}")


from flask import Flask, render_template, request
import requests
import psycopg2
from datetime import datetime

app = Flask(__name__)

# PostgreSQL configuration
DB_CONFIG = {
    'dbname': 'weather_data',
    'user': 'postgres',  # Replace with your PostgreSQL username
    'password': '123456',  # Replace with your PostgreSQL password
    'host': 'localhost',
    'port': 5432
}

# OpenWeatherMap API Key
API_KEY = '4c4567a6b7573ad25f40c085e0ebf302'  # Replace with your API Key


def get_db_connection():
    """Function to connect to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city = None

    if request.method == "POST":
        city = request.form["city"]
        weather_data = get_weather_data(city)
        
        if weather_data:
            # Save weather data to PostgreSQL database
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO weather_history (city, temperature, pressure, humidity, wind_speed, weather, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    city,
                    weather_data["temperature"],
                    weather_data["pressure"],
                    weather_data["humidity"],
                    weather_data["wind_speed"],
                    weather_data["weather"],
                    datetime.now()
                ))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                error = f"Error saving to database: {str(e)}"
        else:
            error = "City not found. Please try again."

    # Retrieve search history from PostgreSQL database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT city, temperature, pressure, humidity, wind_speed, weather, timestamp
            FROM weather_history
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        history = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        history = []
        error = f"Error fetching from database: {str(e)}"

    return render_template("index.html", weather=weather, error=error, city=city, history=history)


def get_weather_data(city):
    """Function to fetch weather data from OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["description"]
        }
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
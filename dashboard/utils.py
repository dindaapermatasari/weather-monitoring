import psycopg2
import pandas as pd

# Database connection details
DB_HOST = "postgres"
DB_NAME = "weather_data"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def get_data():
    """Fetch all data from the PostgreSQL database."""
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

    query = "SELECT * FROM weather"
    df = pd.read_sql_query(query, conn)

    conn.close()
    return df


def kpi_calculations(df):
    """Calculate KPIs based on the data."""
    avg_temp = df["temperature"].mean()
    avg_humidity = df["humidity"].mean()
    max_wind_speed = df["wind_speed"].max()
    total_cities = df["city"].nunique()

    return {
        "avg_temp": avg_temp,
        "avg_humidity": avg_humidity,
        "max_wind_speed": max_wind_speed,
        "total_cities": total_cities,
    }

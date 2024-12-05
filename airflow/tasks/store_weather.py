import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'dbname': 'DB_NAME',
    'user': 'DB_USER',  
    'password': 'DB_PASSWORD',  
    'host': 'DB_HOST',  
    'port': 'DB_PORT'
}

def store(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="fetch_weather")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for record in data:
        cursor.execute(
            """
                INSERT INTO weather (temperature, pressure, humidity, wind_speed, weather, city, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """,
            (
                record["temperature"],
                record["pressure"],
                record["humidity"],
                record["wind_speed"],
                record["weather"],
                record["city"],
            ),
        )
    conn.commit()

    cursor.close()
    conn.close()


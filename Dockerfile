FROM apache/airflow:2.6.0

USER root
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && pip install psycopg2-binary requests

USER airflow


# Pengolahan Data Cuaca

## Deskripsi Proyek

Proyek ini bertujuan untuk mengimplementasikan sistem otomatisasi pengambilan, penyimpanan, dan visualisasi data cuaca menggunakan Apache Airflow, Docker, dan PostgreSQL. Sistem ini mengambil data cuaca dari API OpenWeather untuk beberapa kota, menyimpan data tersebut dalam basis data PostgreSQL yang berjalan di container Docker, dan menampilkan visualisasi data dalam bentuk dashboard interaktif.

## Desain Dashboard

![791031c3-eb35-47f3-8cdb-cc8802a105fb](https://github.com/user-attachments/assets/b5c815df-bd04-4ccc-b2ed-7e365ecf2fb6)

## Alur Kerja 
1. Automasi Data dengan Airflow

- DAG (Directed Acyclic Graph) dibuat menggunakan Apache Airflow untuk mengatur alur kerja otomatisasi.
- DAG terdiri dari beberapa tugas:
    - fetch_weather: Mengambil data cuaca (seperti suhu, kelembapan, kecepatan angin) dari API OpenWeather untuk daftar kota yang telah ditentukan.
    - store_weather: Menyimpan data yang telah diambil ke dalam database PostgreSQL.

2. Penyimpanan Data dengan PostgreSQL di Docker

- PostgreSQL dijalankan di dalam container Docker menggunakan konfigurasi Docker Compose.
- Airflow disambungkan dengan database untuk menyimpan data cuaca yang telah diambil.

3. Visualisasi Data

- Data yang tersimpan dalam database PostgreSQL diakses untuk keperluan visualisasi dashboard menggunakan streamlit.

## Langkah-Langkah Penggunaan

1. Clone repository

```bash
git clone https://github.com/dindaapermatasari/weather-monitoring.git
cd weather-monitoring
```

2. Siapkan Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalasi Dependencies

```bash
pip install -r requirements.txt
```

4. Menjalankan Docker

```bash
docker-compose up -d
```

5. Konfigurasi dan Inisialisasi Airflow

- Inisialisasi database Airflow:
```bash
airflow db init
```
- Jalankan scheduler Airflow:
```bash
airflow scheduler
```
- Jalankan webserver Airflow: 
```bash
airflow webserver
```
- Jalankan Standalone Airflow:
```bash
airflow standalone
```

Setelah itu, akses Airflow melalui browser di http://localhost:8080.

6. Menjalankan Dashboard Visualisasi
```bash
streamlit run dashboard.py
```








<<<<<<< HEAD
# Gunakan image Python sebagai base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin file requirements dan kode aplikasi ke dalam container
COPY requirements.txt requirements.txt
COPY . .

# Instal dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Buka port Flask (default 5000)
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
=======
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

>>>>>>> origin/main
CMD ["python", "app.py"]

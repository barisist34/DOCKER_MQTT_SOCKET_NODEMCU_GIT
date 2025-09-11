# FROM python:3.11-slim-buster

# WORKDIR /app_docker

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . .

# CMD ["python","manage.py","runserver","0.0.0.0:443"]
########################### REDIS DAPHNE #####################
# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt
# COPY . .
####################################################################

############ UVICORN REDIS MQTT WEBSOCKET WEB-DJANGO 250902
# Python image
FROM python:3.11-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Çalışma dizini
WORKDIR /app

# Sistem paketleri
RUN apt-get update && apt-get install -y build-essential libpq-dev net-tools iputils-ping vim dialog

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Uvicorn ile başlat (asgi.py dosyası içinde `application` objesi olduğunu varsayıyoruz)
CMD ["uvicorn", "project_config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

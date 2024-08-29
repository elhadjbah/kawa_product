FROM python:3.11-slim-buster

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer les dépendances système pour mysql (si nécessaire)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install -U pip setuptools wheel
RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir static

COPY . /app/

RUN python manage.py migrate --noinput && python manage.py collectstatic --noinput


EXPOSE 3001

CMD uvicorn kawa_product.asgi:application --host 0.0.0.0 --port 3001
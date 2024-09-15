FROM python:3.11-slim-buster

WORKDIR /app

# set environment variables
ARG SECRET_KEY
ARG DEBUG
ARG ALLOWED_HOSTS_1
ARG ALLOWED_HOSTS_2
ARG CUSTOMER_API_URL
ARG DB_HOST
ARG MYSQL_PORT
ARG MYSQL_ROOT_PASSWORD
ARG MYSQL_DATABASE
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_TEST_DATABASE

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}
ENV ALLOWED_HOSTS_1=${ALLOWED_HOSTS_1}
ENV ALLOWED_HOSTS_2=${ALLOWED_HOSTS_2}
ENV CUSTOMER_API_URL=${CUSTOMER_API_URL}
ENV DB_HOST=${DB_HOST}
ENV MYSQL_PORT=${MYSQL_PORT}
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_TEST_DATABASE=${MYSQL_TEST_DATABASE}

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

COPY . /app/

RUN python manage.py migrate --noinput && python manage.py collectstatic --noinput

EXPOSE 3001

CMD uvicorn kawa_product.asgi:application --host 0.0.0.0 --port 3001
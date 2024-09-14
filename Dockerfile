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
ARG RABBITMQ_HOST
ARG RABBITMQ_PORT

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
ENV RABBITMQ_HOST=${RABBITMQ_HOST:-host.docker.internal}
ENV RABBITMQ_PORT=${RABBITMQ_PORT:-5672}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer les dépendances système pour mysql (si nécessaire)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Mise à jour pip et installation des dépendances
RUN apt-get update

RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install -U pip setuptools wheel
RUN pip install --upgrade pip

COPY requirements.txt /app/

# Installation des dépendances Python
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

# Migration de la base de données et collecte des fichiers statiques
RUN python manage.py migrate --noinput && python manage.py collectstatic --noinput

# Attente de la disponibilité des services externes (ex: base de données, RabbitMQ)
COPY ./wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

EXPOSE 3001

CMD /wait-for.sh ${RABBITMQ_HOST}:${RABBITMQ_PORT} -- uvicorn kawa_product.asgi:application --host 0.0.0.0 --port 3001
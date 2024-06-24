FROM python:3-buster

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install mysql dependencies
RUN apt-get install gcc default-libmysqlclient-dev -y

# Installer les dépendances système pour psycopg2 (si nécessaire)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update

# install dependencies
RUN pip install -U pip setuptools wheel
RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

EXPOSE 3001
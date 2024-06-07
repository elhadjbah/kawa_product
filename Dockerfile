FROM python:3.10-slim-buster

WORKDIR /app

# Installer les dépendances système pour psycopg2 (si nécessaire)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 3001

# Définir la commande de démarrage par défaut
CMD ["uvicorn", "kawa_product.asgi:application", "--host", "0.0.0.0", "--port", "3001", "--workers", "3"]

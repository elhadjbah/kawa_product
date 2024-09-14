#!/bin/sh

HOST_PORT=$1

# Sépare l'hôte et le port
HOST=$(echo $HOST_PORT | cut -d':' -f1)
PORT=$(echo $HOST_PORT | cut -d':' -f2)

while ! nc -z $HOST $PORT; do
  echo "Service $HOST:$PORT is unavailable - sleeping"
  sleep 2
done

echo "Service $HOST:$PORT is now available"
exec "$@"

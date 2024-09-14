#!/bin/sh

HOST=$1
PORT=$2

while ! nc -z $HOST $PORT; do
  echo "Service $HOST:$PORT is unavailable - sleeping"
  sleep 2
done

echo "Service $HOST:$PORT is now available"

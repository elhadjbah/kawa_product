#!/bin/sh

# wait-for.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host"; do
  >&2 echo "Service $host is unavailable - sleeping"
  sleep 2
done

>&2 echo "Service $host is up - executing command"
exec $cmd

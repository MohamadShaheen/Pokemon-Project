#!/usr/bin/env bash
host=$1
shift
port=$1
shift

timeout=15
while ! timeout 1 bash -c "echo > /dev/tcp/$host/$port"; do
  echo "Waiting for $host:$port..."
  sleep 1
  timeout=$((timeout - 1))
  if [ $timeout -le 0 ]; then
    echo "Timeout waiting for $host:$port"
    exit 1
  fi
done

exec "$@"

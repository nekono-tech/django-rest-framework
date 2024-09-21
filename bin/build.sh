#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <container_name>"
  exit 1
fi

CONTAINER_NAME=$1

docker-compose -f compose.dev.yml build $CONTAINER_NAME

#!/bin/bash

docker-compose -f compose.dev.yml down && docker-compose -f compose.dev.yml up -d && docker-compose -f compose.dev.yml logs -f frontend backend

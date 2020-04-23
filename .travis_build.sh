#!/bin/sh

docker build --tag ${HEROKU_REGISTRY_IMAGE} --file ./Dockerfile.prod "."

docker network create -d bridge test-net

docker run -d \
  --name db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=users \
  -p 54321:5432 \
  --network=test-net \
  postgres:12-alpine

docker run -d \
  --name app \
  -e "PORT=8765" \
  -e "DATABASE_TEST_URL=postgresql://postgres:postgres@db:5432/users" \
  -p 5002:8765 \
  --network=test-net \
  $HEROKU_REGISTRY_IMAGE;
#!/bin/sh

docker build --tag ${HEROKU_REGISTRY_IMAGE} --file ./Dockerfile.prod "."

docker network create -d bridge test-net

docker run -d \
  --name db \
  -e POSTGRES_USER=$DATABASE_TEST_USER \
  -e POSTGRES_PASSWORD=$DATABASE_TEST_PASSWORD \
  -e POSTGRES_DB=$DATABASE_TEST_NAME \
  -p 5432:5432 \
  --network=test-net \
  postgres:12-alpine
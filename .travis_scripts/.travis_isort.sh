#!/bin/sh

docker exec app isort project/**/*.py --check-only;
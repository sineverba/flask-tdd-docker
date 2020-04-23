#!/bin/sh

docker exec app python -m pytest "project/tests";
#docker exec app flake8 project;
#docker exec app black project --check;
#docker exec app isort project/**/*.py --check-only;
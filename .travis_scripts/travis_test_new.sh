#!/bin/sh

docker exec app python -m pytest "project/tests";

docker exec app /home/myuser/.local/bin/black project --check;

docker exec app /home/myuser/.local/bin/flake8 project;

docker exec app /home/myuser/.local/bin/isort project/**/*.py --check-only;
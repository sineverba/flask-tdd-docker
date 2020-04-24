#!/bin/sh

docker exec app /home/myuser/.local/bin/isort project/**/*.py --check-only;
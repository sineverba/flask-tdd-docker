# Flask TDD + Docker

#### Test Status   

[![Build Status](https://api.travis-ci.com/sineverba/flask-tdd-docker.svg?branch=master)](https://travis-ci.com/sineverba/flask-tdd-docker)

#### Code Coverage

[![Coverage Status](https://coveralls.io/repos/github/sineverba/flask-tdd-docker/badge.svg?branch=master)](https://coveralls.io/github/sineverba/flask-tdd-docker?branch=master) [![codecov](https://codecov.io/gh/sineverba/flask-tdd-docker/branch/master/graph/badge.svg)](https://codecov.io/gh/sineverba/flask-tdd-docker)

## Setup dependencies

``` bash
#$ sudo add-apt-repository ppa:deadsnakes/ppa - if necessary
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget
$ sudo apt install python3.8 python3-pip python3-setuptools python3.8-venv -y
#$ sudo add-apt-repository --remove ppa:deadsnakes/ppa
```


#### Launch Docker

``` bash

$ docker-compose up -d

```

#### Create and seed the database

```
$ docker-compose exec users python manage.py recreate_db
$ docker-compose exec users python manage.py seed_db
```

#### Run test

``` bash
$ docker-compose exec users python -m pytest "project/tests" --cov="project"
```

##### Run unit test in parallel

``` bash
$ docker-compose exec users pytest "project/tests/test_users_unit.py" -k "unit" -n 4
```

#### Run linter (Flake8 + Black + isort)

``` bash
$ docker-compose exec users flake8 project
$ docker-compose exec users black project --check
$ docker-compose exec users black project --diff
$ docker-compose exec users black project
$ docker-compose exec users /bin/sh -c "isort project/**/*.py --check-only"
$ docker-compose exec users /bin/sh -c "isort project/**/*.py --diff"
$ docker-compose exec users /bin/sh -c "isort project/**/*.py"
```

---------------------------------------------------------------

## Start app from local

``` bash

$ docker run -d --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=users -p 5432:5432 postgres:12-alpine
$ source env/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=project/__init__.py
$ export FLASK_ENV=development
$ export APP_SETTINGS=project.config.DevelopmentConfig
$ export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/users
$ export DATABASE_TEST_URL=postgresql://postgres:postgres@localhost:5432/users
$ flask shell
$ python manage.py recreate_db
$ gunicorn -b 0.0.0.0:5000 manage:app --daemon
$ pkill gunicorn

``` 

---------------------------------------------------------------

## Heroku main commands

### Build the image

`$ docker build -f Dockerfile.prod -t registry.heroku.com/<app_name>/web .`

### Push the image

`$ docker push registry.heroku.com/<app_name>/web:latest`

### Spin the image

`$ heroku container:release web -a <app_name>`
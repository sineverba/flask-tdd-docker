# Flask TDD + Docker

#### Test Status   

![Travis (.com)](https://img.shields.io/travis/com/sineverba/flask-tdd-docker?label=Travis%20CI&style=flat-square)

#### Code Coverage

![Coveralls github branch](https://img.shields.io/coveralls/github/sineverba/flask-tdd-docker/master?label=Coveralls&style=flat-square) ![Codecov branch](https://img.shields.io/codecov/c/github/sineverba/flask-tdd-docker/master?label=Codecov&style=flat-square)

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

## Heroku main commands

### Build the image

`$ docker build -f Dockerfile.prod -t registry.heroku.com/<app_name>/web .`

### Push the image

`$ docker push registry.heroku.com/<app_name>/web:latest`

### Spin the image

`$ heroku container:release web -a <app_name>`
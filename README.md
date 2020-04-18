## Setup dependencies

``` bash
#$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget
$ sudo apt install python3.8 python3-pip python3-setuptools python3.8-venv -y
#$ sudo add-apt-repository --remove ppa:deadsnakes/ppa
```

### First install

``` bash

$ python3.8 -m venv env
$ source env/bin/activate
(env) pip install -r requirements.txt
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
$ docker-compose exec users python -m pytest "project/tests"
```

---------------------------------------------------------------

## Heroku main commands

### Build the image

`$ docker build -f Dockerfile.prod -t registry.heroku.com/<app_name>/web .`

### Push the image

`$ docker push registry.heroku.com/<app_name>/web:latest`

### Spin the image

`$ heroku container:release web -a <app_name>`

------------------------------------------------------------

## Python useful commands

### Save requirements

`(env) $ pip freeze > requirements.txt`

### Set executable

`$ chmod +x entrypoint.sh`
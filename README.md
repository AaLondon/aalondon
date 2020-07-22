# Contributing to aalondon

The following are instructions on how to contribute to this project.

# Prerequisites

## Docker

In order to make it easier to maintain the project we only support developers using
docker. 

Development is done in a docker container that is built with docker compose, so
you will need to obtain and install docker and docker compose.

See <https://docs.docker.com/get-docker/> for installation instructions for
your operating system.

## Follow this sequence to get up and running

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml run web python manage.py migrate
docker-compose -f docker-compose.yml run web python manage.py createsuperuser
docker-compose -f docker-compose.yml run web python manage.py cms_setup
docker-compose -f docker-compose.yml run web python manage.py loaddata physical_meetings
docker-compose -f docker-compose.yml run web python manage.py loaddata online_meetings
npm install
npm run build
```
Go to http://0.0.0.0:8000/

## Postgres Database in docker

If you need to drop and recreate the postgres database in your docker container do the following:

```bash
docker-compose -f docker-compose.yml run web python manage.py dbshell
```
in psql shell

```psql
aalondon=# \c postgres
postgres=# DROP DATABASE aalondon;
postgres=# CREATE DATABASE aalondon;
postgres=# exit
```

## Running the unit test testsuite

```bash
docker-compose -f docker-compose.yml run web python manage.py test --verbosity=2
```

or if you have GNU Make,

```bash
make test
```

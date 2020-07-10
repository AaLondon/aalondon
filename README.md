# Contributing to aalondon

The following are instructions on how to contribute to this project.

# Prerequisites

## Docker

Development is done in a docker container that is built with docker compose, so
you will need to obtain and install docker and docker compose.

See <https://docs.docker.com/get-docker/> for installation instructions for
your operating system.

## PostgreSQL database

1. Obtain the postgres database from one of the existing contributors of this
   project. (Mention filename `aalondon.sql`)

2. Save this in repository root directory.

# Docker  

## First time build

1. Start docker

2. Run `docker-compose up` from command line

3. Using `docker container list`, identify the {web_container_id} of the
   aalondon_web docker image. You'll need this for the next step.

3. Load in the postgres db using the following commands:

```bash
# kill the docker container
docker stop {web_container_id}

# set up database table ready for data import
docker exec -it {db_container_id} psql -U postgres -d postgres -c "DROP DATABASE aalondon;"
docker exec -it {db_container_id} psql -U postgres -d postgres -c "CREATE DATABASE aalondon;"
docker exec -it {db_container_id} psql -U postgres -d postgres -c "CREATE ROLE aalondon;"

# import database
cat aalondon.sql | docker exec -i {db_container_id} psql -U postgres -d aalondon
```

## After first time build

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml run web python manage.py createsuperuser
docker-compose -f docker-compose.yml run web python manage.py import_zoom_csv
npm install
npm run build
```

Go to http://0.0.0.0:8000/


FROM python:3.7-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Build dependencies.
ARG buildDeps=" \
build-essential \
libpq-dev \
"

# Project dependencies
ARG deps=" \
gdal-bin \
gettext \
postgresql-client \
git \
"

# Install build dependencies and project dependencies
RUN set -ex \
       && apt-get update \
       && apt-get install -y $buildDeps $deps --no-install-recommends

# pip install step
COPY requirements.txt requirements.txt
RUN set -ex \
       && pip install --no-cache-dir -r requirements.txt \
       && rm -rf requirements.txt /var/lib/apt/lists/*

# Strip the build dependencies from the image
RUN set -ex \
       && apt-get purge -y && apt-get purge -y --auto-remove $buildDeps

WORKDIR /code
COPY . /code/
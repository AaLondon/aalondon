FROM python:3.7-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# GNUPG is needed to fetch PostgreSQL package from Debian repos.
RUN set -ex; \
	if ! command -v gpg > /dev/null; then \
		apt-get update; \
		apt-get install -y --no-install-recommends \
			gnupg \
			dirmngr \
		; \
		rm -rf /var/lib/apt/lists/*; \
	fi

# Add PostgreSQL gpg key to keyring.
RUN set -ex; \
# pub   4096R/ACCC4CF8 2011-10-13 [expires: 2019-07-02]
#       Key fingerprint = B97B 0AFC AA1A 47F0 44F2  44A0 7FCC 7D46 ACCC 4CF8
# uid                  PostgreSQL Debian Repository
	key='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8'; \
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
	gpg --batch --export "$key" > /etc/apt/trusted.gpg.d/postgres.gpg; \
	rm -rf "$GNUPGHOME"; \
	apt-key list


# Add PostgreSQL repo.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main $PG_MAJOR" > /etc/apt/sources.list.d/pgdg.list
	

# Build dependencies.
ARG buildDeps=" \
build-essential \
libpq-dev \
"

# Project dependencies
ARG deps=" \
gdal-bin \
gettext \
postgresql-client-11 \
git \
"

# Install build dependencies and project dependencies.
# The build dependencies are only needed for the pip install step.
RUN set -ex \
       && apt-get update \
       && apt-get install -y $buildDeps $deps --no-install-recommends


# pip install step.
# Install Python library dependencies from requirements.txt
COPY requirements.txt requirements.txt
RUN set -ex \
       && pip install --no-cache-dir -r requirements.txt \
       && rm -rf requirements.txt /var/lib/apt/lists/*

# Strip the build dependencies from the image.
RUN set -ex \
       && apt-get purge -y && apt-get purge -y --auto-remove $buildDeps \
       $(! command -v gpg > /dev/null || echo 'gnupg dirmngr')


WORKDIR /code
COPY . /code/

# Contributing to aalondon

Thank you for taking an interest in aa-london. We welcome any contribution you can give.
Please fork this repository and create any pull requests from aa-london in your repository.

# Site Architecture
The site is run on [Python](Python.org) using [Django](https://www.djangoproject.com/) with [Wagtail](https://wagtail.io/) as its CMS. Our database is [Postgresql](https://www.postgresql.org/).
For our frontend we have a number of [React](https://reactjs.org/) components.
If you are not familiar with these technologies then we highly recommend going through their respective tutorials
before contributing.

# Setup options
You can get up and running using [Docker](https://www.docker.com/) or running your development environment locally.If you are running locally you will need to have Postgresql>=12 and Python>=3.8 installed.  


## Docker

In order to make it easier to maintain the project we do have a docker
container, but it is really a personal preference. If you wish you can instead
follow the instructions in section "Virtualenv".

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

If you need to drop and recreate the postgres database in your docker container
do the following:

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


## Linux/OSX

You may choose to use Virtualenv instead of docker. The following are details
on how to get set up with Python Virtualenv. You will need Python3 and Python3
Virtualenv already installed and a locally running Postgresql>=12 running.


```bash
sudo apt-get install python3-virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo -u postgres -i
```

Enter postgresql shell

(Substitute 'john' with your own username that you wish to use postgres with).

```psql
psql
CREATE ROLE john with LOGIN SUPERUSER;
exit # exit psql
```

Resume bash session

```bash
exit # exit sudo -u postgres -i
createdb aalondon

python manage.py migrate
python manage.py createsuperuser # add details
python manage.py cms_setup
python manage.py crawl # load physical meetings
python manage.py loaddata online_meetings

npm install
npm run build

python manage.py runserver # launch application
```

The application is now running at <https://127.0.0.1:8000>.

### Whenever you change the model

Run the following:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will trigger Django to autogenerate a 'migration file' which will need to
be added to version control.

### Shell

This will launch an iPython interpreter with all the web application's modules
and data loaded. Extremely useful for debugging / prototyping.

```
python manage.py shell_plus
```

### Testing

We try hard to make sure our code has great test coverage and ask that when you provide pull requests
you also provide tests where appropriate.

To see if your code change is not covered by a test you can use coverage.

```bash
coverage run -m pytest
coverage html
```
The first line runs the test suite and the second provides an html report of coverage.
This is located here htmlcov/index.html


# Running the unit test testsuite

```bash
docker-compose -f docker-compose.yml run web python manage.py test --verbosity=2
```

or if you have GNU Make,

```bash
make test
```



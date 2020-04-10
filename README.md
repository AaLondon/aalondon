
# Docker  

## Run these commands to get up and running

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml run web python manage.py createsuperuser
docker-compose -f docker-compose.yml run web python manage.py import_zoom_csv
npm install
npm run build

```

Go to http://0.0.0.0:8000/


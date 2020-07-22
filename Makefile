# Run the unit test testsuite
all:
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml up -d

test:
	docker-compose -f docker-compose.yml run web python manage.py test --verbosity=2

# Run the unit test testsuite
test:
	docker-compose -f docker-compose.yml run web python manage.py test --verbosity=2

#!/usr/bin/env sh

docker-compose exec web python manage.py loaddata fixtures.json
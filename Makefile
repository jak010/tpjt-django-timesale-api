
SRC=./src
DOCKER=./docker

DJANGO_SETTINGS_MODEL=config.settings.local

PYTHONPATH=$(PWD)/src

run.docker:
	docker-compose -f ./.docker/docker-compose.yml up

run.local:
	python $(SRC)/manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODEL)


migrations:
	python $(SRC)/manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODEL)

migrate:
	python $(SRC)/manage.py migrate --settings=$(DJANGO_SETTINGS_MODEL)



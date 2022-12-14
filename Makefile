DOCKER_REGISTRY := registry.hub.docker.com
DOCKER_NAME := icij/prophecies
PWD := `pwd`
CURRENT_VERSION ?= `poetry version -s`

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install-pip install-yarn

install-dev: install-pip-dev install-yarn

install-pip-dev:
		poetry install --with dev

install-pip:
		poetry install

install-yarn:
		yarn

migrate:
		poetry run python manage.py migrate

makemigrations:
		poetry run python manage.py makemigrations

run:
		poetry run python manage.py runserver 0.0.0.0:8008

update:
	  poetry update
		yarn upgrade

test: test-back test-front

test-back:
		poetry run python manage.py test --settings=prophecies.settings.test

test-front:
		yarn test:unit


# Requires the `entr` binary (can be installed with apt)
entr-test:
		find . -name '*.py' | entr poetry run python manage.py test --settings=prophecies.settings.test

webpack-build:
		yarn build

webpack-serve:
		yarn serve

shell:
		poetry run python manage.py shell

createsuperuser:
		poetry run python manage.py createsuperuser

minor:
		poetry version minor -n

major:
		poetry version major -n

patch:
		poetry version patch -n

publish:
		poetry publish

build:
		poetry build

docker-build:
		docker build -t $(DOCKER_NAME) .

docker-tag:
		docker tag $(DOCKER_NAME) $(DOCKER_NAME):${CURRENT_VERSION}
		docker tag $(DOCKER_NAME) $(DOCKER_REGISTRY)/$(DOCKER_NAME):${CURRENT_VERSION}
		docker tag $(DOCKER_NAME) $(DOCKER_REGISTRY)/$(DOCKER_NAME):latest

docker-push:
		docker push $(DOCKER_NAME):${CURRENT_VERSION}
		docker push $(DOCKER_NAME):latest

docker-publish: docker-build docker-tag docker-push

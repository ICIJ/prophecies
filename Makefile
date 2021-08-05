DOCKER_REGISTRY := registry.cloud.icij.org
DOCKER_NAME := prophecies
PWD := `pwd`
CURRENT_VERSION ?= `python -c "from prophecies import __version__ ; print(__version__)"`

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install-pip install-yarn

install-pip:
		pipenv install

install-yarn:
		yarn

migrate:
		pipenv run python manage.py migrate

makemigrations:
		pipenv run python manage.py makemigrations

run:
		pipenv run python manage.py runserver 0.0.0.0:8008

test:
		pipenv run python manage.py test --settings=prophecies.settings.test

# Requires the `entr` binary (can be installed with apt)
entr-test:
		find . -name '*.py' | entr pipenv run python manage.py test --settings=prophecies.settings.test

webpack-build:
		yarn build

webpack-serve:
		yarn serve

shell:
		pipenv run python manage.py shell

createsuperuser:
		pipenv run python manage.py createsuperuser

minor:
		pipenv run bumpversion --commit --tag --current-version ${CURRENT_VERSION} minor prophecies/__init__.py

major:
		pipenv run bumpversion --commit --tag --current-version ${CURRENT_VERSION} major prophecies/__init__.py

patch:
		pipenv run bumpversion --commit --tag --current-version ${CURRENT_VERSION} patch prophecies/__init__.py

docker-build:
		docker build -t $(DOCKER_NAME) .

docker-tag:
		docker tag $(DOCKER_NAME) $(DOCKER_REGISTRY)/$(DOCKER_NAME):${CURRENT_VERSION}
		docker tag $(DOCKER_NAME) $(DOCKER_REGISTRY)/$(DOCKER_NAME):latest

docker-push:
		docker push $(DOCKER_REGISTRY)/$(DOCKER_NAME):${CURRENT_VERSION}
		docker push $(DOCKER_REGISTRY)/$(DOCKER_NAME):latest

docker-publish: docker-build docker-tag docker-push

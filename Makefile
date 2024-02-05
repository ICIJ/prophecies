CURRENT_VERSION := $(shell poetry version -s)
SEMVERS := major minor patch
FRONT_PREFIX := prophecies/apps/frontend

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

$(SEMVERS):
		poetry version $@
		npm version --prefix ${FRONT_PREFIX} $@
		$(MAKE) tag-version

set-version:
		poetry version ${CURRENT_VERSION}
		npm version ${CURRENT_VERSION} --prefix ${FRONT_PREFIX}
		$(MAKE) tag-version

tag-version:
		git commit -m "build: bump to v${CURRENT_VERSION}" pyproject.toml ${FRONT_PREFIX}/package.json
		git tag v${CURRENT_VERSION}

poetry-build:
		poetry build	

build: webpack-build poetry-build
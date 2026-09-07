CURRENT_VERSION := $(shell uv version --short)
SEMVERS := major minor patch
FRONT_PREFIX := prophecies/apps/frontend

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install-pip install-yarn

install-dev: install-pip-dev install-yarn

install-pip-dev:
		uv sync

install-pip:
		uv sync --no-dev

install-yarn:
		yarn

migrate:
		uv run python manage.py migrate

makemigrations:
		uv run python manage.py makemigrations

run:
		uv run python manage.py runserver 0.0.0.0:8008

update:
	  uv lock --upgrade
		yarn upgrade

test: test-back test-front

test-back:
		uv run python manage.py test --settings=prophecies.settings.test

test-front:
		yarn test:unit


# Requires the `entr` binary (can be installed with apt)
entr-test:
		find . -name '*.py' | entr uv run python manage.py test --settings=prophecies.settings.test

webpack-build:
		yarn build

webpack-serve:
		yarn serve

shell:
		uv run python manage.py shell

createsuperuser:
		uv run python manage.py createsuperuser

$(SEMVERS):
		uv version --bump $@
		npm version --prefix ${FRONT_PREFIX} $@
		$(MAKE) tag-version

set-version:
		uv version ${CURRENT_VERSION}
		npm version ${CURRENT_VERSION} --prefix ${FRONT_PREFIX}
		$(MAKE) tag-version

tag-version:
		git commit -m "build: bump to v${CURRENT_VERSION}" pyproject.toml uv.lock ${FRONT_PREFIX}/package.json
		git tag v${CURRENT_VERSION}

uv-build:
		uv build

build: webpack-build uv-build

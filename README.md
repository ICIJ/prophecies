# Prophecies

An ICIJ app to conduct data validation and cleaning.

| | Status |
| ---: | --- |
| **CI checks** | [![CircleCI](https://img.shields.io/circleci/build/github/ICIJ/prophecies?token=db6cce793b346e91b82e04bd38fac2af48fc3164)](https://circleci.com/gh/ICIJ/prophecies/tree/main) |
| **Docker** | [![Docker](https://img.shields.io/docker/v/icij/prophecies?color=%2350ca22)](https://hub.docker.com/repository/docker/icij/prophecies) |
| **Code Climate** | [![Maintainability](https://img.shields.io/codeclimate/maintainability/ICIJ/prophecies)](https://codeclimate.com/github/ICIJ/prophecies/maintainability) |

## Installation

Required:

* Python 3.8
* Node 14.x
* Pipenv 11.x
* Yarn 1.x

To setup a virtualenv with `Pipenv` and to install required packages:

```bash
make install
```

To setup the database:

```bash
make migrate
```

To create a superuser:

```bash
make createsuperuser
```

For more customization, this app utilizes [12factor](https://www.12factor.net/)
inspired environment variables to configure your Django application. You can
create `.env` file using the custom settings variables:

```
DEBUG=on
DATABASE_URL=
CACHE_URL=dummycache://
STATIC_URL=/static/
SOCIAL_AUTH_PROVIDER_KEY=
SOCIAL_AUTH_PROVIDER_SECRET=
SOCIAL_AUTH_PROVIDER_HOSTNAME=http://localhost:3001
SOCIAL_AUTH_PROVIDER_USERNAME_FIELD=uid
SOCIAL_AUTH_PROVIDER_GROUPS_FIELD=groups_by_applications.prophecies
SOCIAL_AUTH_PROVIDER_STAFF_GROUP=icijstaff
```

## Run

To run app inside its virtualenv, use the following command:

```bash
make run
```

Then in a separated terminal, build and serve assets with Webpack:

```
make webpack-serve
```

Then visit [http://0.0.0.0:9009](http://0.0.0.0:9009)

## Publishing a new Docker image

Run **one** of these commands depending on the kind of version you need to publish:

```
pipenv run bumpversion build # will increment the build number (x.y.z-build0 →  x.y.z-build1)
pipenv run bumpversion release # will increment to the next release part (alpha →  beta →  rc)
pipenv run bumpversion patch
pipenv run bumpversion minor
pipenv run bumpversion major
```

Then the new tag on Github. The CI will take care of shipping the new version on Docker Hub:

```
git push origin main --tags
git push origin main
```

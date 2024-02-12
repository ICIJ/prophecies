# Prophecies

An ICIJ app to conduct data validation and cleaning.

| | Status |
| ---: | --- |
| **CI checks** | [![](https://img.shields.io/github/actions/workflow/status/icij/prophecies/main.yml)](https://github.com/ICIJ/prophecies/actions) |
| **Docker** | [![Docker](https://img.shields.io/docker/v/icij/prophecies?color=%2350ca22)](https://hub.docker.com/repository/docker/icij/prophecies) |
| **Code Climate** | [![Maintainability](https://img.shields.io/codeclimate/maintainability/ICIJ/prophecies)](https://codeclimate.com/github/ICIJ/prophecies/maintainability) |

## Installation

Required:

* Python 3.10
* Node 16.x
* Poetry >= 1.2
* Yarn 1.x

To setup a virtualenv with `poetry` and to install required packages:

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
make webpack-build
make run
``` 

Then in a separated terminal, build and serve assets with Webpack:

```
make webpack-serve
```

Then visit [http://0.0.0.0:9009](http://0.0.0.0:9009)

### Run tests

To run the back end tests
```
make test-back
```
To run the front end tests

```
make test-front
```

To run all tests

```
make test
```

## Publishing a new Docker image manually

Run **one** of these commands depending on the kind of version you need to publish:

```
make build # will build the pip deliverables (.egg, .tgz)
make patch # will increment to the next release part (alpha →  beta →  rc)
make minor
make major
make publish # will publish on pypi
```

Then the new tag on Github. The CI will take care of shipping the new version on Docker Hub:

```
git push origin main --tags
git push origin main
```

# Prophecies

An ICIJ app to conduct data validation and cleaning.

## Installation

Required:

* Python 3.8
* Node 12.x
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

Run **one** of these commands while ICIJ internal VPN is running:

```
make patch docker-publish
make minor docker-publish
make major docker-publish
```

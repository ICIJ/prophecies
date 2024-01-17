FROM python:3.9 AS poetry
FROM node:18 AS webpack

RUN mkdir /frontend/
WORKDIR /frontend/
COPY ./prophecies/apps/frontend/ /frontend/

RUN yarn config set network-timeout 300000
RUN yarn --non-interactive --production=false
RUN yarn build

FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PORT 8008
ENV POETRY_VERSION 1.7.1
ENV POETRY_HOME "/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV POETRY_NO_INTERACTION  1
ENV PATH "$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - -y --version $POETRY_VERSION

RUN mkdir /code/
WORKDIR /code

COPY . /code/
COPY --from=webpack /frontend/dist/ /code/prophecies/apps/frontend/dist/

RUN poetry install
RUN poetry run python manage.py collectstatic --noinput

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /usr/bin/wait
RUN chmod +x /usr/bin/wait
    
CMD /usr/bin/wait && poetry run gunicorn prophecies.wsgi -b 0.0.0.0:${PORT:-8008}

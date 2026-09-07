FROM node:18 AS webpack

RUN mkdir /frontend/
WORKDIR /frontend/
COPY ./prophecies/apps/frontend/ /frontend/

RUN yarn config set network-timeout 300000
RUN yarn --non-interactive --production=false
RUN yarn build

FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PORT 8008
ENV UV_PROJECT_ENVIRONMENT "/code/.venv"
ENV PATH "/code/.venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE "prophecies.settings.production"

COPY --from=ghcr.io/astral-sh/uv:0.9.10 /uv /usr/local/bin/uv

RUN mkdir /code/
WORKDIR /code

COPY . /code/
COPY --from=webpack /frontend/dist/ /code/prophecies/apps/frontend/dist/

RUN uv sync --frozen --no-dev
RUN python manage.py collectstatic --noinput

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /usr/bin/wait
RUN chmod +x /usr/bin/wait
    
CMD /usr/bin/wait && gunicorn prophecies.wsgi -b 0.0.0.0:${PORT:-8008}

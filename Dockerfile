FROM node:18 AS webpack

RUN mkdir /frontend/
WORKDIR /frontend/
COPY ./prophecies/apps/frontend/ /frontend/

RUN yarn
RUN yarn build

FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PORT 8008

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir /code/
WORKDIR /code

COPY . /code/
COPY --from=webpack /frontend/dist/ /code/prophecies/apps/frontend/dist/

RUN /root/.local/bin/poetry install
RUN /root/.local/bin/poetry run python manage.py collectstatic --noinput

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /usr/bin/wait
RUN chmod +x /usr/bin/wait
    
CMD /usr/bin/wait && /root/.local/bin/poetry run gunicorn prophecies.wsgi -b 0.0.0.0:${PORT:-8008}

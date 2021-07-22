FROM node:14 AS webpack

RUN mkdir /frontend/
WORKDIR /frontend/
COPY ./prophecies/apps/frontend/ /frontend/

RUN yarn
RUN yarn build

FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PORT 8008

RUN pip3 install pipenv

RUN mkdir /code/
WORKDIR /code

COPY . /code/
COPY --from=webpack /frontend/dist/ /code/prophecies/apps/frontend/dist/

RUN pipenv install
RUN pipenv run python manage.py collectstatic --noinput

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /usr/bin/wait
RUN chmod +x /usr/bin/wait

CMD /usr/bin/wait && pipenv run gunicorn prophecies.wsgi -b 0.0.0.0:${PORT:-8008}

FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN pip3 install pipenv

RUN mkdir /code/
WORKDIR /code

COPY . /code/
RUN pipenv install --python 3.6
RUN pipenv run python manage.py compilescss
RUN pipenv run python manage.py collectstatic --noinput

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /usr/bin/wait
RUN chmod +x /usr/bin/wait

CMD /usr/bin/wait && pipenv run python manage.py runserver 0.0.0.0:${PORT:-8000}

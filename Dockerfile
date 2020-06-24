FROM python:3.7-alpine
MAINTAINER akewan

ENV PYTHONUNBUFFERRED 1

COPY ./requirements.txt /requirements.txt

# to be able to install psycopg2>=2.7.5,<2.8.0
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# delete temp requirements
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app

COPY ./app /app

RUN adduser -D akewan

USER akewan

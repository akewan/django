FROM python:3.8-slim
MAINTAINER akewan

ENV PYTHONUNBUFFERRED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app

COPY ./app /app

RUN adduser -D akewan

USER akewan

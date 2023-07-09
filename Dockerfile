FROM python:3.11-alpine

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY app/app /app
WORKDIR /app
EXPOSE 8000

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
       build-base \
       gcc \
       musl-dev \
       python3-dev \
       libffi-dev \
       openssl-dev \
       cargo \
       rust

RUN apk add --no-cache libpq

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

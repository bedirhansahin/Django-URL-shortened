FROM python:3.11-alpine

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY app/app /app
WORKDIR /app
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

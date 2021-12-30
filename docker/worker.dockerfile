# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./docker/celery/worker/start.sh /start-worker.sh
RUN sed -i 's/\r$//g' /start-worker.sh
RUN chmod +x /start-worker.sh

COPY ./docker/celery/beat/start.sh /start-beat.sh
RUN sed -i 's/\r$//g' /start-beat.sh
RUN chmod +x /start-beat.sh


COPY . .

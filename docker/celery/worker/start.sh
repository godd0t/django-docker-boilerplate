#!/bin/sh
set -e
set -x

celery -A django_docker_boilerplate worker -l INFO
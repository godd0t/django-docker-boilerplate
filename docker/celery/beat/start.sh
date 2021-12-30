#!/bin/sh
set -e
set -x
rm -f './celerybeat.pid'
rm -f './celerybeat-schedule'
celery -A django_docker_boilerplate beat -l INFO
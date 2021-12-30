#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

find * -prune -type d | while IFS= read -r d; do
    rm -rf "$d/migrations"
done
find * -prune -type d | while IFS= read -r d; do
    python manage.py makemigrations "$d" --noinput
done
python manage.py makemigrations --noinput
python manage.py migrate
# dev only
python manage.py createsuperuser --username admin --email admin@gmail.com --noinput
exec "$@"

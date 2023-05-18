#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "ejecutando makemigrations..."
python3 manage.py makemigrations

echo "ejecutando migrate..."
python3 manage.py migrate

echo "ejecutando collect-static..."
python3 manage.py collectstatic --no-input

echo "ejecutando loaddata..."
python3 manage.py loaddata --exclude auth.permission --exclude contenttypes ./fixtures/db.xml

exec "$@"
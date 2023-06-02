#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "ejecutando flush..."
python manage.py flush --no-input

echo "ejecutando makemigrations..."
python3 manage.py makemigrations

echo "ejecutando migrate mainApp..."
python3 manage.py migrate mainApp

echo "ejecutando collect-static..."
python3 manage.py collectstatic --no-input --clear

echo "ejecutando migrate..."
python3 manage.py migrate

echo "ejecutando loaddata..."
python3 manage.py loaddata -v3 ./fixtures/db.json

python3 manage.py runserver 0.0.0.0:8000
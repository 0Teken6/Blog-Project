#!/bin/sh

echo "Running migrations..."
python manage.py migrate

python manage.py collectstatic --noinput
python manage.py populate_db  

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000

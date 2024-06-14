#!/bin/sh

set -e

echo "Making migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Creating superuser..."
python create_superuser.py

exec "$@"

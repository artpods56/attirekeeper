#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Making migrations..."
python manage.py makemigrations --noinput    
python manage.py migrate --noinput
    
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear    

echo "Creating superuser..."
python create_superuser.py

exec "$@"
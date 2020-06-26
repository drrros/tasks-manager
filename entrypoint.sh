#!/bin/sh


python manage.py collectstatic --noinput --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput
rm /code/celerybeat.pid
# start celery worker
celery worker --app=tasks_manager.celery:app --loglevel=INFO &
# start celery beat
celery beat --app=tasks_manager.celery:app --loglevel=INFO &

exec "$@"

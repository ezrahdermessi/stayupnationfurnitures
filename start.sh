#!/bin/bash
python manage.py collectstatic --noinput --clear
python manage.py migrate
gunicorn stayup_furniture.wsgi:application --bind 0.0.0.0:${PORT:-8080} --timeout 120

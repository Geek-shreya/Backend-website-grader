#!/bin/bash
python manage.py collectstatic --noinput
waitress-serve --port=8000 mongodbb.wsgi:application  # Use a specific port

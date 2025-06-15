#!/bin/sh

set -e

python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec "$@"
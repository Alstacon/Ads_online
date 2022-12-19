#!/bin/bash
python manage.py loadall
exec "$@"
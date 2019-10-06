#!/bin/sh
# For gunicorn
mkdir ./logs
. ../bin/activate
gunicorn --bind 0.0.0.0:5000 --access-logfile ./logs/access --error-logfile ./logs/error wsgi:app

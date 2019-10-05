#!/bin/sh
# For gunicorn
. ../bin/activate
gunicorn --bind 0.0.0.0:5000 --access-logfile ./WSGIlog.txt wsgi:app

#!/usr/bin/env bash
gunicorn -w $WORKERS -b 0.0.0.0:5000 -k gevent wsgi:app
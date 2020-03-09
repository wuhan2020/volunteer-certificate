#!/bin/bash
# start up shell script
nohup ~/.local/bin/gunicorn --log-level info -p /tmp/gunicorn-vc.pid --bind localhost:5000 wsgi:app >>~/logs/volunteer-certificate.log &

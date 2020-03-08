#!/bin/bash
# start up shell script
nohup gunicorn --bind localhost:5000 app:app >>~/logs/volunteer-certificate.log &

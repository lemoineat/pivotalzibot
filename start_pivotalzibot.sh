#!/bin/sh

cd /usr/local/share/pivotalzibot/
gunicorn --workers=3 --bind 127.0.0.1:5001 main:app

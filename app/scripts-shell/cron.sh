#!/bin/sh

# python /app/manage.py runscript jobs_reset
env > /app/.env
crond -f -l 2
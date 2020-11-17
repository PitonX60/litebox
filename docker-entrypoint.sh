#!/bin/bash

set -e

if [[ "$CRON" = "1" ]]; then
    echo "RUN CRON JOB"
    crontab /package/crontab
    cron /package/crontab
fi

python3 manage.py migrate
pip3 uninstall --yes django-firebird
pip3 install --use-feature=2020-resolver https://github.com/PitonX60/django-firebird/archive/v2.2.a1.fork.zip

exec "$@"
#!/bin/bash
SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export ENVIRONMENT=DEVELOPMENT
export COUNTLY_APP_KEY_MOBILE_NONPROD_OVERRIDE=secret
export COUNTLY_APP_KEY_WEBAPP_NONPROD_OVERRIDE=secret
export FLASK_APP=dhos_trustomer_api/autoapp.py
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}
export TRUSTOMER_CONFIG_MOUNT="./trustomer-config-dummy"

if [ -z "$*" ]
then
  python -m dhos_trustomer_api
else
  flask $*
fi

#!/bin/bash
#
# Create wheelhouse cache to speed up test_scaffold runs.
# Builds a wheelhouse folder containing al dependencies.
#

if type virtualenv-3.4 ; then
    VIRTUALENV=virtualenv-3.4
else
    VIRTUALENV=virtualenv
fi

set -e
set -x
rm -rf /tmp/wheelhouse-venv
rm -rf wheelhouse
$VIRTUALENV --no-site-packages -p python3.4 /tmp/wheelhouse-venv
source /tmp/wheelhouse-venv/bin/activate
# default pip is too old for 3.4
# https://github.com/jnrbsn/daemonocle/issues/8
pip install -U pip
pip install .[test,dev]
pip install wheel
pip freeze > /tmp/wheelhouse-venv/requirements.txt
# websauna 0.0 development not available, remove from freeze
echo "$(grep -v "websauna" /tmp/wheelhouse-venv/requirements.txt)" >/tmp/wheelhouse-venv/requirements.txt
# sed -i '/websauna/d' /tmp/wheelhouse-venv/requirements.txt
# Needed for Daemonocle
pip wheel -r /tmp/wheelhouse-venv/requirements.txt
#!/usr/bin/env bash

apt-get update -y
# Python dev packages
apt-get install -y build-essential python python-dev
# python-setuptools being installed manually
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python

apt-get install -y git

if ! command -v psql; then
    apt-get install -y postgresql-9.1 libpq-dev
fi

if ! command -v pip; then
    easy_install -U pip
fi
pip install -r /vagrant/requirements.txt
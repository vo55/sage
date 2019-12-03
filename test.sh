#!/usr/bin/env bash
pip install --user virtualenv
python3 -m virtualenv env

./env/bin/pip3 install -r requirements-dev.txt
./env/bin/python3 -m unittest discover ./sage-tests -p '*_tests.py'

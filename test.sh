#!/usr/bin/env bash
pip install --user virtualenv
python3 -m virtualenv env

./env/bin/pip3 install -r requirements.txt
./env/bin/pip3 unittest ./sage-tests/

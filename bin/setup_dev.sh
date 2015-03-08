#!/bin/bash

virtualenv env
. env/bin/activate
pip install -r requirements-dev.txt --use-mirrors

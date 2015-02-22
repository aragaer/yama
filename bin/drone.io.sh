#!/bin/bash -ex

pip install -q -r requirements-dev.txt --use-mirrors
nosetests
behave -c

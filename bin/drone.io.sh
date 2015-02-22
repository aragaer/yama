#!/bin/bash -ex

pip install -r requirements-dev.txt
nosetests
behave -c

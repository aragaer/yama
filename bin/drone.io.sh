#!/bin/bash -ex

echo "deb http://toolbelt.heroku.com/ubuntu ./" | sudo tee /etc/apt/sources.list.d/heroku.list
wget -O- https://toolbelt.heroku.com/apt/release.key | sudo apt-key add -
sudo apt-get -qq update #-o Dir::Etc::sourcelist="sources.list.d/heroku.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"
sudo apt-get -qq install foreman 
pip install -q -r requirements-dev.txt --use-mirrors
nosetests
behave -c

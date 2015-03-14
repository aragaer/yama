#!/usr/bin/env python3

from datetime import date
import json
import os

from bottle import Bottle, request, response
from mongomock import MongoClient

from yama.storage import Storage


APP = Bottle()
STORAGE = Storage(MongoClient().db)


def _get_timeline():
    for container in STORAGE.get_root_containers():
        if container.label == 'timeline':
            return container
    return STORAGE.create_container('timeline')


def _get_date_container(date):
    timeline = _get_timeline()
    for container in timeline.children:
        if container.label == date:
            return container
    return timeline.create_child(date)


@APP.post('/memos/daily')
def daily():
    message = request.body.read().decode('utf-8')
    str_date = date.today().isoformat()
    _get_date_container(str_date).post(message)


@APP.get('/memos/daily/<date>')
def daily_memos(date):
    response.content_type = 'application/json'
    return json.dumps(_get_date_container(date).messages)


@APP.route('/')
def hello():
    return 'Hello, world'


if __name__ == '__main__':
    print(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

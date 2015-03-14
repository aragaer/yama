#!/usr/bin/env python3

from datetime import date
import json
import os

from bottle import Bottle, request, response

from yama.storage import Storage


APP = Bottle()
STORAGE = None


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


@APP.get('/memos/daily/<isodate>')
def daily_memos(isodate):
    response.content_type = 'application/json'
    if isodate == 'today':
        isodate = date.today().isoformat()
    return json.dumps(_get_date_container(isodate).messages)


@APP.route('/')
def hello():
    return 'Hello, world'


def _get_mongo_connection():
    mongo_url = os.environ.get('MONGO_URL')

    if mongo_url:
        from urllib.parse import urlparse
        from pymongo import Connection
        conn = Connection(mongo_url)
        return conn[urlparse(mongo_url).path[1:]]
    else:
        from mongomock import MongoClient
        return MongoClient().db


if __name__ == '__main__':
    STORAGE = Storage(_get_mongo_connection())
    APP.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

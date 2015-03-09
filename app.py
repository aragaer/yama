#!/usr/bin/env python3

import json

from bottle import Bottle, response

from yama.storage import Storage


APP = Bottle()
STORAGE = Storage()


@APP.route('/memos/daily/<date>')
def daily_memos(date):
    response.content_type = 'application/json'
    return json.dumps(STORAGE.get_container(date).messages)


@APP.route('/')
def hello():
    return 'Hello, world'


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)

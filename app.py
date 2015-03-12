#!/usr/bin/env python3

from datetime import date
import json
import os

from bottle import Bottle, request, response

from yama.storage import Storage


APP = Bottle()
STORAGE = Storage()

@APP.post('/memos/daily')
def daily():
    message = request.body.read().decode('utf-8')
    str_date = date.today().isoformat()
    STORAGE.get_container(str_date).post(message)


@APP.get('/memos/daily/<date>')
def daily_memos(date):
    response.content_type = 'application/json'
    return json.dumps(STORAGE.get_container(date).messages)


@APP.route('/')
def hello():
    return 'Hello, world'


if __name__ == '__main__':
    print(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

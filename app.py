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

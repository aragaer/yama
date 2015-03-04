#!/usr/bin/env python3

import os

from bottle import route, run

@route('/')
def hello_world():
    return 'Hello, world'

if __name__ == '__main__':
    run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

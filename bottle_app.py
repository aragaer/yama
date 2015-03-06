#!/usr/bin/env python3

import os

from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello_world():
    return 'Hello, world'

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

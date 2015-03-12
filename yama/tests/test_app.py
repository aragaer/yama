#!/usr/bin/env python3

from io import BytesIO
import json
import os
import sys
import unittest

from bottle import response, request, tob
from freezegun import freeze_time

from yama.storage import Storage

PATH_TESTS = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.basename(PATH_TESTS)
PATH_CURRENT = PATH_TESTS.strip(PATH_PROJECT)

sys.path.append(PATH_CURRENT)

import app


class AppTest(unittest.TestCase):

    def test_daily_memos_should_return_json(self):
        app.daily_memos('2015-01-01')
        self.assertEquals(response.content_type, 'application/json')

    def test_daily_memos_should_return_messages_from_container(self):
        container = app.STORAGE.get_container('2015-01-01')
        messages = ['test message', 'another test message']
        for message in messages:
            container.post(message)

        result = app.daily_memos('2015-01-01')

        self.assertEquals(json.loads(result), messages)

    def test_daily_memos_should_post_to_container(self):
        container = app.STORAGE.get_container('2015-03-12')

        body = tob("Just another test line")
        post_data = BytesIO()
        post_data.write(body)
        post_data.seek(0)
        request.environ['CONTENT_LENGTH'] = str(len(body))
        request.environ['wsgi.input'] = post_data

        with freeze_time('2015-03-12'):
            app.daily()

        self.assertEquals(['Just another test line'], container.messages)

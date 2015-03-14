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

    def setUp(self):
        from mongomock import MongoClient
        app.STORAGE = Storage(MongoClient().db)

    def _get_timeline_container(self):
        for container in app.STORAGE.get_root_containers():
            if container.label == 'timeline':
                return container
        return app.STORAGE.create_container('timeline')

    def _get_date_container(self, date):
        timeline = self._get_timeline_container()
        for container in timeline.children:
            if container.label == date:
                return container
        return timeline.create_child(date)

    def test_daily_memos_should_return_json(self):
        app.daily_memos('2015-01-01')
        self.assertEquals(response.content_type, 'application/json')

    def test_daily_memos_should_return_messages_from_container(self):
        container = self._get_date_container('2015-01-01')
        messages = ['test message', 'another test message']
        for message in messages:
            container.post(message)

        result = app.daily_memos('2015-01-01')

        self.assertEquals(json.loads(result), messages)

    def test_daily_memos_should_post_to_container(self):
        container = self._get_date_container('2015-03-12')

        body = tob("Just another test line")
        post_data = BytesIO()
        post_data.write(body)
        post_data.seek(0)
        request.environ['CONTENT_LENGTH'] = str(len(body))
        request.environ['wsgi.input'] = post_data

        with freeze_time('2015-03-12'):
            app.daily()

        self.assertEquals(['Just another test line'], container.messages)

    def test_today(self):
        container = self._get_date_container('2015-03-14')
        messages = ['test message', 'another test message']
        for message in messages:
            container.post(message)

        with freeze_time('2015-03-14'):
            result = app.daily_memos('today')

        self.assertEquals(json.loads(result), messages)

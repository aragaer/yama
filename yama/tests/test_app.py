#!/usr/bin/env python3

import json
import os
import sys
import unittest

from bottle import response

from yama.storage import Storage

PATH_TESTS = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.basename(PATH_TESTS)
PATH_CURRENT = PATH_TESTS.strip(PATH_PROJECT)

sys.path.append(PATH_CURRENT)

import app


class AppTest(unittest.TestCase):

    def test_dailyMemosShouldReturnJson(self):
        app.daily_memos('2015-01-01')
        self.assertEquals(response.content_type, 'application/json')

    def test_dailyMemosShouldReturnMessagesFromContainer(self):
        container = app.STORAGE.get_container('2015-01-01')
        messages = ['test message', 'another test message']
        for message in messages:
            container.post(message)

        result = app.daily_memos('2015-01-01')

        self.assertEquals(json.loads(result), messages)

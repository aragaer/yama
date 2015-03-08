#!/usr/bin/env python3

import unittest

from mongomock import MongoClient

from yama.container import Container
from yama.storage import Storage


class ContainerTest(unittest.TestCase):

    def test_should_accept_posted_messages(self):
        container = Container()

        container.post('A message')

        self.assertIn('A message', container.messages)

    def test_has_label(self):
        container = Container('a name')

        self.assertEquals(container.label, 'a name')


class MongoStorageTest(unittest.TestCase):

    _connection = None

    def setUp(self):
        self._connection = MongoClient().db
        self._storage = Storage(self._connection)

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

    def test_child_containers(self):
        container = Container('root')

        child = container.create_child('subcontainer')

        self.assertIsInstance(child, Container)
        self.assertEqual('subcontainer', child.label)

        self.assertEqual([child], container.children)


class MongoStorageTest(unittest.TestCase):

    _connection = None
    _storage = None

    def _connect(self):
        self._storage = Storage(self._connection)

    def _reconnect(self):
        self._storage = Storage(self._connection)

    def setUp(self):
        self._connection = MongoClient().db
        self._connect()

    def test_loading(self):
        child = Container('child')
        container = Container(storage=self._storage,
                              contents=['a message', 'other message'],
                              children=[child])
        self.assertEqual(['a message', 'other message'],
                         container.messages)
        self.assertEqual(['child'], [c.label for c in container.children])

    def test_child_is_persistent(self):
        container = self._storage.create_container('container')
        child = container.create_child('child')
        child.post('a message')

        self._reconnect()

        container = next(self._storage.get_root_containers())
        child = container.children[0]
        self.assertEqual(['a message'], child.messages)

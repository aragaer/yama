#!/usr/bin/env python3

import unittest

from mongomock import MongoClient

from yama.storage import Storage


class StorageTest(unittest.TestCase):

    _connection = None

    def setUp(self):
        self._connection = MongoClient().db

    def test_create_container(self):
        storage = Storage(self._connection)

        container = storage.create_container('container name')

        self.assertEquals(container.label, 'container name')

    def test_empty_storage(self):
        storage = Storage(self._connection)
        self.assertEqual(sum(1 for _ in storage.get_container_ids()), 0)

    def test_container_ids(self):
        storage = Storage(self._connection)
        container = storage.create_container('container')

        ids = [cid for cid in storage.get_container_ids()]
        self.assertEqual(len(ids), 1)

        container_id = ids[0]
        container2 = storage.get_container(container_id)

        self.assertEqual(container, container2)

        storage2 = Storage(self._connection)
        ids = [cid for cid in storage.get_container_ids()]
        self.assertEqual(len(ids), 1)

        container3 = storage2.get_container(container_id)

        self.assertIsNotNone(container3)
        self.assertEqual(container3.label, 'container')

    def test_is_persistent(self):
        storage = Storage(self._connection)
        container = storage.create_container('container name')
        container.post('Test message')

        storage2 = Storage(self._connection)
        container2 = storage2.get_container(next(storage.get_container_ids()))

        self.assertIn('Test message', container2.messages)

    def test_stores_container_messages(self):
        storage = Storage(self._connection)
        storage.create_container('container name')
        container_id = next(storage.get_container_ids())

        storage.post_message('message', container_id)

        storage = Storage(self._connection)
        container = storage.get_container(container_id)
        self.assertIn('message', container.messages)

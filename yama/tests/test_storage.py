#!/usr/bin/env python3

import unittest

from mongomock import MongoClient

from yama.storage import Storage
from yama.container import Container


class StorageTest(unittest.TestCase):

    _connection = None
    _storage = None

    def setUp(self):
        self._connection = MongoClient().db
        self._connect()

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
        container.create_child('inner')

        storage = Storage(self._connection)
        container = next(storage.get_root_containers())

        self.assertEquals(['Test message'], container.messages)

        container.post('another one')

        storage = Storage(self._connection)
        container = next(storage.get_root_containers())

        self.assertEquals(['Test message', 'another one'], container.messages)
        # self.assertEquals(['inner'], [c.label for c in container.children])

    def test_stores_container_messages(self):
        storage = Storage(self._connection)
        storage.create_container('container name')
        container_id = next(storage.get_container_ids())

        storage.post_message('message', container_id)

        storage = Storage(self._connection)
        container = storage.get_container(container_id)
        self.assertIn('message', container.messages)

    def test_stores_subcontainers(self):
        container = self._storage.create_container('root')
        child = Container('child')

        self._storage.store_container_child(child, container.id)

        self._reconnect()
        container = next(self._storage.get_root_containers())

        self.assertEqual(['child'], [c.label for c in container.children])

    def test_root_containers(self):
        storage = Storage(self._connection)
        container = storage.create_container('root 1')
        container2 = storage.create_container('root 2')

        roots = [c for c in storage.get_root_containers()]
        self.assertEqual([container, container2], roots)

        storage = Storage(self._connection)
        roots = [c for c in storage.get_root_containers()]

        self.assertEqual(len(roots), 2)
        self.assertEqual(['root 1', 'root 2'], [c.label for c in roots])

    def _connect(self):
        self._storage = Storage(self._connection)

    def _reconnect(self):
        self._storage = Storage(self._connection)

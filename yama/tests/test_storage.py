#!/usr/bin/env python3

import unittest

from yama.container import Container
from yama.storage import Storage


class StorageTest(unittest.TestCase):

    def test_canGetContainer(self):
        storage = Storage()

        container = storage.get_container('container name')

        self.assertIsInstance(container, Container)

    def test_sameNameReturnsSameContainer(self):
        storage = Storage()

        container1 = storage.get_container('container name')
        container2 = storage.get_container('container name')
        container3 = storage.get_container('other name')

        self.assertEqual(container1, container2)
        self.assertNotEqual(container1, container3)

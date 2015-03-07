#!/usr/bin/env python3

import unittest

from yama.container import Container
from yama.storage import Storage


class StorageTest(unittest.TestCase):

    def test_canGetContainer(self):
        storage = Storage()

        container = storage.get_container('container name')

        self.assertIsInstance(container, Container)

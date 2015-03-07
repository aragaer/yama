#!/usr/bin/env python3

import os
import sys
import unittest

from yama.storage import Storage

PATH_TESTS = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.basename(PATH_TESTS)
PATH_CURRENT = PATH_TESTS.strip(PATH_PROJECT)

sys.path.append(PATH_CURRENT)

from app import APP


class AppTest(unittest.TestCase):

    def test_shouldHaveStorage(self):
        self.assertIsNotNone(APP.storage)
        self.assertIsInstance(APP.storage, Storage)

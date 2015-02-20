#!/usr/bin/env python3

import os
import unittest

from testfixtures import tempdir

from config_reader import ConfigReader


class ConfigReaderTest(unittest.TestCase):

    _path = None

    def setUp(self):
        self._path = os.getcwd()
        self.addCleanup(lambda: os.chdir(self._path))

    @tempdir()
    def test_shouldReadPath(self, directory):
        directory.write("oneliner.config", b"path = ./lines\n")
        os.chdir(directory.path)
        reader = ConfigReader()

        reader.read()

        self.assertEqual(reader.path, os.path.join(directory.path, "lines"))

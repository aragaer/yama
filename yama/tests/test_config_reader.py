#!/usr/bin/env python3

import os
import unittest

from testfixtures import tempdir

from yama.config_reader import ConfigReader


class ConfigReaderTest(unittest.TestCase):

    _path = None

    def setUp(self):
        self._path = os.getcwd()
        self.addCleanup(lambda: os.chdir(self._path))

    @tempdir()
    def test_should_read_path(self, directory):
        directory.write("oneliner.config", b"path = ./lines\n")
        os.chdir(directory.path)
        reader = ConfigReader()

        reader.read()

        self.assertEqual(reader.path, os.path.join(directory.path, "lines"))

    @tempdir()
    def test_should_read_absolute_path(self, directory):
        newpath = os.path.join(directory.path, "lines")
        directory.write("oneliner.config",
                        bytes("path = "+newpath+"\n", 'utf-8'))
        os.chdir(directory.path)
        reader = ConfigReader()

        reader.read()

        self.assertEqual(reader.path, os.path.join(directory.path, "lines"))

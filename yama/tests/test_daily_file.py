#!/usr/bin/env python3

import os
import unittest

from freezegun import freeze_time
from testfixtures import tempdir, compare

from yama.oneliner import Writer, main


class DailyFileTest(unittest.TestCase):

    @freeze_time("2015-02-17")
    @tempdir()
    def test_should_create_new_file(self, directory):
        writer = Writer(directory.path)
        directory.write("gold.txt", b'test string\n')

        writer.write("test string")

        directory.check("2015-02-17.txt", "gold.txt")
        compare(directory.read("gold.txt"), directory.read("2015-02-17.txt"))

    @freeze_time("2015-02-17")
    @tempdir()
    def test_should_append_to_existing_file(self, directory):
        writer = Writer(directory.path)
        directory.write("2015-02-17.txt", b'line one\n')
        directory.write("gold.txt", b'line one\nline two\n')

        writer.write("line two")

        directory.check("2015-02-17.txt", "gold.txt")
        compare(directory.read("gold.txt"), directory.read("2015-02-17.txt"))


class MainTest(unittest.TestCase):

    _path = None

    def setUp(self):
        self._path = os.getcwd()
        self.addCleanup(lambda: os.chdir(self._path))

    @freeze_time("2015-02-17")
    @tempdir()
    def test_executeMain(self, directory):
        import sys

        os.chdir(directory.path)
        directory.makedir("some_dir")
        directory.write("oneliner.config", b"path = ./some_dir")
        directory.write("gold.txt", b'test string\n')

        sys.argv = ['oneliner', 'test', 'string']
        main()

        directory.check("gold.txt", "oneliner.config", "some_dir")
        compare(directory.read("gold.txt"),
                directory.read("some_dir/2015-02-17.txt"))

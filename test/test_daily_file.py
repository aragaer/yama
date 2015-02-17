#!/usr/bin/env python3

import unittest

from freezegun import freeze_time
from testfixtures import tempdir, compare

from oneliner import Writer


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

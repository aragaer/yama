#!/usr/bin/env python3

import unittest

from yama.message import Message


class MessageTest(unittest.TestCase):

    def test_has_string(self):
        message = Message('test string')

        self.assertEqual(message.text, 'test string')

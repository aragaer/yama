#!/usr/bin/env python3

import unittest

from yama.container import Container


class ContainerTest(unittest.TestCase):

    def test_shouldAcceptPostedMessages(self):
        container = Container()

        container.post('A message')

        self.assertIn('A message', container.messages)

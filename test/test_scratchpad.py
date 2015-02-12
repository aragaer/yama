#!/usr/bin/env python3

import os
import unittest

from scratchpad import Scratchpad


class ScratchPadTest(unittest.TestCase):

    def tearDown(self):
        os.remove('.scratchpad')

    def test_shouldAddMessages(self):
        scratchpad = Scratchpad()
        scratchpad.post("test")
    
    def test_shouldReturnMessages(self):
        scratchpad = Scratchpad()
        scratchpad.post("test")
        messages = [m for m in scratchpad.messages]
        self.assertEqual(messages, ["test"])
        
    def test_shouldStoreMultipleMessages(self):
        scratchpad = Scratchpad()
        scratchpad.post("test")
        scratchpad.post("post")

        messages = [m for m in scratchpad.messages]
        self.assertEquals(messages, ["test", "post"])
    
    def test_shouldStorePersistently(self):
        scratchpad = Scratchpad()
        scratchpad.post("test")
        scratchpad2 = Scratchpad()
        
        messages = [m for m in scratchpad2.messages]
        self.assertEqual(messages, ["test"])
 

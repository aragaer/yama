#!/usr/bin/env python3


class Scratchpad(object):

    _messages = None

    def __init__(self):
        try:
            with open('.scratchpad', 'r') as storage:
                self._messages = [m.rstrip() for m in storage.readlines()]
        except OSError:
            self._messages = []

    def post(self, message):
        self._messages.append(message)
        with open('.scratchpad', 'a') as storage:
            storage.write(message+"\n")

    @property
    def messages(self):
        for message in self._messages:
            yield message

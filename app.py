#!/usr/bin/env python3

from yama.storage import Storage


class OnelinerApp(object):

    _storage = None

    def __init__(self):
        self._storage = Storage()

    @property
    def storage(self):
        return self._storage


APP = OnelinerApp()

#!/usr/bin/env python3

from yama.container import Container


class Storage(object):

    _containers = None

    def __init__(self):
        self._containers = {}

    def get_container(self, str_container_name):
        if str_container_name not in self._containers:
            self._containers[str_container_name] = Container()

        return self._containers[str_container_name]

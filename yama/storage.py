#!/usr/bin/env python3

from yama.container import Container


class Storage(object):

    def get_container(self, str_container_name):
        return Container()

#!/usr/bin/env python3

import os


class ConfigReader(object):

    _path = None

    def read(self):
        with open(os.path.join(os.getcwd(), "oneliner.config")) as config:
            for line in config.readlines():
                if '=' in line:
                    key, val = (s.strip() for s in line.split('='))
                    if key == 'path':
                        self._path = os.path.abspath(val)

    @property
    def path(self):
        return self._path

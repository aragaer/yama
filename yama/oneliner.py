#!/usr/bin/env python3

from datetime import date
from os import path
import sys

from yama.config_reader import ConfigReader


__all__ = ['Writer', 'main']


class Writer(object):

    _path = None

    def __init__(self, storage_path):
        self._path = storage_path

    def write(self, line):
        filename = date.today().isoformat()+".txt"
        filepath = path.join(self._path, filename)
        with open(filepath, "a+") as out:
            out.write(line+"\n")


def main():
    config = ConfigReader()
    config.read()
    Writer(config.path).write(" ".join(sys.argv[1:]))

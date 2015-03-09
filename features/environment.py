#!/usr/bin/env python3

import os
import sys

from webtest import TestApp

path_features = os.path.abspath(os.path.dirname(__file__))
path_project = os.path.basename(path_features)
path_current = path_features.strip(path_project)

sys.path.append(path_current)

from app import APP, STORAGE


def before_feature(context, feature):
    context.app = TestApp(APP)
    context.storage = STORAGE

    context.debug = True


def after_scenario(context, scenario):
    if 'background_processes' in context:
        for process in context.background_processes:
            try:
                process.terminate()
            except ProcessLookupError:
                pass

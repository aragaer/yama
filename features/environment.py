#!/usr/bin/env python3

import os
import sys

from webtest import TestApp

path_features = os.path.abspath(os.path.dirname(__file__))
path_project = os.path.basename(path_features)
path_current = path_features.strip(path_project)

sys.path.append(path_current)

from app import APP


def before_feature(context, feature):
    context.app = TestApp(APP)
    context.storage = APP.storage

    context.debug = True

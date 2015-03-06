#!/usr/bin/env python3

import unittest

from bottle import yieldroutes

import bottle_app


ALL_ROUTES = dict((route.rule, route.callback)
                  for route in bottle_app.app.routes)


class RouteTest(unittest.TestCase):

    def test_shouldRouteHello(self):
        self.assertIn('/hello', ALL_ROUTES.keys())


class HelloTest(unittest.TestCase):

    def test_shouldReturnHello(self):
        callback = ALL_ROUTES['/hello']
        self.assertEqual(callback(), "Hello, world")

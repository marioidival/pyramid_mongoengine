from __future__ import unicode_literals

import unittest
from pyramid import testing


class PyramidMongoEngineTestCase(unittest.TestCase):

    def setUp(self):

        request = testing.DummyRequest()

        self.config = testing.setUp(
            request=request,
        )

        """
        Test with routes
        def test_my_function(self):
            from pyramid import testing
            with testing.testConfig() as config:
                config.add_route('bar', '/bar/{id}')
                my_function_which_needs_route_bar()
        """

    def tearDown(self):
        testing.tearDown()

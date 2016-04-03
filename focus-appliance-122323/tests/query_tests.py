import os
import unittest

import mock as mock
from google.appengine.ext import testbed

from fhired.FHIRQueries import FHIRQueries


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    @mock.patch('urllib2.urlopen')
    def test_get_all_conditions(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'Encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        encounters = FHIRQueries().get_all_patients_conditions(4)

        self.assertIsNotNone(encounters)
        self.assertEqual(65, len(encounters))

    def tearDown(self):
        self.testbed.deactivate()

if __name__ == "__main__":
    unittest.main()

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
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        encounters = FHIRQueries().get_all_patients_conditions(4)

        self.assertIsNotNone(encounters)
        self.assertEqual(65, len(encounters))

    @mock.patch('urllib2.urlopen')
    def test_get_single_patient_id_by_name(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_single.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRQueries().get_patient_id_by_name("Acosta")

        self.assertIsNotNone(patient_ids)
        self.assertListEqual(["57"], patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_get_multi_patient_id_by_name(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_multiple.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRQueries().get_patient_id_by_name("Paul")

        self.assertIsNotNone(patient_ids)
        self.assertListEqual(["57","222"], patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_get_patient_by_id(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_single.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient = FHIRQueries().get_patient_by_id("57")

        self.assertIsNotNone(patient)
        self.assertEqual(57, patient.pt_id)

    @mock.patch('urllib2.urlopen')
    def test_get_patient_by_querying_id(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_single.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patients = FHIRQueries().get_patient_for(query={'_id': '57'})

        self.assertIsNotNone(patients)
        self.assertEqual(57, patients[0].pt_id)

    def tearDown(self):
        self.testbed.deactivate()

if __name__ == "__main__":
    unittest.main()

import os
import unittest

from google.appengine.ext import testbed
from mock import mock

from fhired.FHIRed_Up import FHIRedUp


class FHIRedUpTests(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()

    @mock.patch('urllib2.urlopen')
    def test_get_single_patient_by_id(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_single.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().get_patient_by_id(57)

        self.assertIsNotNone(patient_ids)

    def tearDown(self):
        self.testbed.deactivate()

    @mock.patch('urllib2.urlopen')
    def test_get_get_candidate_hccs_for(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_single.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().get_candidate_hccs_for("57", 1, 4)

        self.assertIsNotNone(patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_risks_scores_list(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'patient_single.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().risks_scores_list("57", 2016, False, False)

        self.assertIsNotNone(patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_get_hccs(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().get_hccs(57, 2016)

        self.assertIsNotNone(patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_find_missing_diagnoses_by_patient_id(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().find_missing_diagnoses_by_patient_id(57, 2016)

        self.assertIsNotNone(patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_risks_scores_distribution(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().risks_scores_distribution(57, 2016, False, False)

        self.assertIsNotNone(patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_get_candidate_hccs_for(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().get_candidate_hccs_for(57, 5, False)

        self.assertIsNotNone(patient_ids)

    @mock.patch('urllib2.urlopen')
    def test_get_current_risk_score_for_pt(self, m_urlopen):
        response_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'encounter.json')

        with open(os.path.normpath(response_name), mode='rb') as response:
            m_urlopen().read.return_value = response.read()

        patient_ids = FHIRedUp().get_current_risk_score_for_pt(57, False)

        self.assertIsNotNone(patient_ids)

    def test_add_hcc_candidate_for(self):
        up = FHIRedUp()

        up.add_hcc_candidate_for(57, 1, [], "", "confirm")
        hcc = up.view_current_hcc_for(57, 1)

        self.assertIsNotNone(hcc)

        up.delete_hcc_for(57, 1)


    def tearDown(self):
        self.testbed.deactivate()
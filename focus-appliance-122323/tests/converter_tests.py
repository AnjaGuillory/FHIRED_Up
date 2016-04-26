import unittest

from fhired.SnowmedConverter import SnowmedConverter


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.converter = SnowmedConverter

    def test_convert_snowmed_to_hcc(self):
        hcc = self.converter.to_hcc('151004')

        self.assertIsNotNone(hcc)
        self.assertEquals('3', hcc[0])
        self.assertEquals('Central Nervous System Infection', hcc[1])

    def test_n_hcc_convert_snowmed_to_hcc(self):
        hcc = self.converter.to_hcc('147001')

        self.assertIsNone(hcc)

    def test_fail_convert_snowmed_to_hcc(self):
        hcc = self.converter.to_hcc('000000')

        self.assertIsNone(hcc)

    def test_convert_from_hcc(self):
        snowmed = self.converter.from_hcc(hcc="3")

        self.assertEqual(443, len(snowmed))

    def test_fail_convert_from_hcc(self):
        snowmed = self.converter.from_hcc(hcc="-3")

        self.assertEqual(0, len(snowmed))

    def test_gt_hcc_details(self):
        hccDetails = self.converter.get_hcc_details("-3")
        
        self.assertEqual(None, hccDetails)


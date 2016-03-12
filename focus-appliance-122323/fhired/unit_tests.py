import unittest

from fhired.LookupTables import LookupTables


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.tables = LookupTables()

    def test_icd9_hcc_lookup(self):
        assert self.tables.icd9_to_hcc('037') == 'TETANUS'

    def test_hcc_risk_score(self):
        assert self.tables.hcc_to_risk_score(181) == 'Chemotherapy'

    def test_hcc_risk_value(self):
        assert self.tables.hcc_to_risk_score_value(164) == 4.42

    def test_snowmed_icd9_lookup(self):
        assert self.tables.snowmed_to_icd9(422088007) == '648.80'

    def test_snowmed_hcc_lookup(self):
        assert self.tables.snowmed_to_hcc(422088007) == (147, 'ABN GLUCOSE IN PREG-UNSP')
        assert self.tables.snowmed_to_hcc(155855008) is None

if __name__ == "__main__":
    unittest.main()

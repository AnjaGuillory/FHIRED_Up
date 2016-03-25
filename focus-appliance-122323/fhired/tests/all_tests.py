import unittest

from fhired.tests.entity_tests import EntityTests
from fhired.tests.lookup_tests import LookupTests
from fhired.tests.query_tests import QueryTests

tests = [unittest.TestLoader().loadTestsFromTestCase(LookupTests),
         unittest.TestLoader().loadTestsFromTestCase(QueryTests),
         unittest.TestLoader().loadTestsFromTestCase(EntityTests), ]

for test in tests:
    unittest.TextTestRunner().run(test)

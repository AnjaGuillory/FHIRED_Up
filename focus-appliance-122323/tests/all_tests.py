import unittest

from lookup_tests import LookupTests
from query_tests import QueryTests
from entity_tests import EntityTests
from converter_tests import ConverterTests

tests = [unittest.TestLoader().loadTestsFromTestCase(LookupTests),
         unittest.TestLoader().loadTestsFromTestCase(QueryTests),
         unittest.TestLoader().loadTestsFromTestCase(EntityTests),
         unittest.TestLoader().loadTestsFromTestCase(ConverterTests)]

for test in tests:
    unittest.TextTestRunner().run(test)

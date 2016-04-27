import unittest

from lookup_tests import LookupTests
from query_tests import QueryTests
from entity_tests import EntityTests
from converter_tests import ConverterTests
from up_tests import FHIRedUpTests
from user_tests import UserTests

tests = [unittest.TestLoader().loadTestsFromTestCase(LookupTests),
         unittest.TestLoader().loadTestsFromTestCase(QueryTests),
         unittest.TestLoader().loadTestsFromTestCase(EntityTests),
         unittest.TestLoader().loadTestsFromTestCase(ConverterTests),
         unittest.TestLoader().loadTestsFromTestCase(FHIRedUpTests),
         unittest.TestLoader().loadTestsFromTestCase(UserTests)]

for test in tests:
    unittest.TextTestRunner().run(test)

import unittest

from fhired.Entities import Patient


class EntityTests(unittest.TestCase):
    def setUp(self):
        self.test_resource = {'id': '0000000001',
                              'birthDate': '01/01/1970',
                              'gender': 'male',
                              'name': [
                                  {
                                      'given': 'John',
                                      'family': 'Smith'
                                  },
                              ],
                              'address': [
                                  {
                                      'use': 'home',
                                      'line': '1500 N Verdugo Rd',
                                      'city': 'Glendale',
                                      'state': 'CA',
                                      'postalCode': '91208'
                                  },
                                  {
                                      'use': 'work',
                                      'line': '1900 Pico Blvd',
                                      'city': 'Santa Monica',
                                      'state': 'CA',
                                      'postalCode': '90405'
                                  },
                              ],
                              }

    def test_init_from_resource(self):
        patient = Patient.init_from_fhir_patient_resource(self.test_resource)

        self.assertEqual(1, patient.pt_id)
        self.assertEqual('John Smith', patient.name)
        self.assertEqual('01/01/1970', patient.dob)
        self.assertEqual('male', patient.gender)
        self.assertDictEqual({'use': 'home','line': '1500 N Verdugo Rd','city': 'Glendale',
                              'state': 'CA','postalCode': '91208'
                              }, patient.address)
        self.assertIsNone(patient.list_of_diag)


if __name__ == "__main__":
    unittest.main()

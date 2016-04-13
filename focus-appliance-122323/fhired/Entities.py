from SnowmedConverter import SnowmedConverter
from fhired.FHIRQueries import *


def get_current_year():
    return 2014  # there is no data for 2016


class Patient:
    def __init__(self, pt_id, name, dob, gender, address):
        self.pt_id = pt_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.__diagnoses_list = None
        self.__risk_score = None

    def get_diagnoses_list(self):
        """Uses the patient ID to get the list of SNOMED
           codes for that patient's conditions from the FHIR server"""
        if self.__diagnoses_list is None:
            from fhired.FHIRQueries import FHIRQueries
            queries = FHIRQueries()
            self.__diagnoses_list = queries.get_all_patients_conditions(self.pt_id)
        # The output of this query is a list:
        # [EncounterID, EncounterServiceYear, [list of [ConditionCode, ConditionName, ConditionCodingSystem]]]
        return self.__diagnoses_list

    @staticmethod
    def init_from_fhir_patient_resource(resource):
        """Initialize a patient object from a FHIR Patient Resource record.
        
        Args:
            resource: a FHIR Patient Resource

        Returns:
            Entities.Patient
        """
        patient = Patient(int(resource['id']), '', '', '', '')

        if 'birthDate' in resource: patient.dob = resource.get('birthDate')
        if 'gender' in resource: patient.gender = resource.get('gender')

        # format the name           
        if 'name' in resource and len(resource['name']) > 0:
            if 'given' in resource['name'][0]: patient.name = ' '.join(resource['name'][0].get('given'))
            if 'family' in resource['name'][0]: patient.name += ' ' + ' '.join(resource['name'][0].get('family'))

        # format address (use "home" address only)
        address = {}
        if 'address' in resource:
            for a in resource['address']:
                if a.get('use') == 'home':
                    if 'line' in a: address['line'] = a.get('line')
                    if 'city' in a: address['city'] = a.get('city')
                    if 'state' in a: address['state'] = a.get('state')
                    if 'postalCode' in a: address['postalCode'] = a.get('postalCode')

                    break
        patient.address = address

        return patient


class Provider:
    def __init__(self, prov_id, name, list_of_patients):
        self.prov_id = prov_id
        self.name = name
        self.listOfPatients = list_of_patients


class Hcc:
    def __init__(self, code, date, name, risk_score, notes):
        self.code = code
        self.name = name
        self.date = date
        self.risk_score = risk_score
        self.notes = notes


class RiskDistribution:
    def __init__(self, name, risk_score):
        self.name = name
        self.risk_score = risk_score

    def for_chart(self):
        return {"name": self.name, "y": self.risk_score}

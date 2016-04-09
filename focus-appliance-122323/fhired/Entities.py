﻿from datetime import date
from SnowmedConverter import SnowmedConverter


class Patient:
    def __init__(self, pt_id, name, dob, gender, address, starting_year):
        self.pt_id = pt_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address

        # TODO: It may be helpful if these three properties were loaded when needed (ie: lazy load) rather than every time a patient object is instantiated.
        self.list_of_diag = self.set_diagnoses_list()
        self.list_of_cand_hccs = self.set_cand_hccs_list()  # TODO: Getting the candidate HCCs should include the parameters "years" and "include_rejected".
        self.risk_score = self.cal_risk_score(starting_year)

    def set_diagnoses_list(self):
        """Uses the patient ID to get the list of SNOMED
           codes for that patient's conditions from the FHIR server"""
        from fhired.FHIRQueries import FHIRQueries
        queries = FHIRQueries()
        # The output of this query is a list:
        # [EncounterID, EncounterServiceYear, [list of [ConditionCode, ConditionName, ConditionCodingSystem]]]
        return queries.get_all_patients_conditions(self.pt_id)
        
    def set_cand_hccs_list(self):
        """ Gets a list of candidate hccs  to set 
            for the patient"""
        from fhired.FHIRQueries import FHIRQueries
        queries = FHIRQueries()
        # TODO: The params passed to get_candidate_hccs_for() for "years" and "include_rejected" should be dynamic.
        return queries.get_candidate_hccs_for(self.pt_id, 3, False)

    def cal_risk_score(self, starting_year):
        '''Calculates the patient's risk score for the 
           year entered as a parameter'''
        risk_score = 0
        already_added_hccs = []
        converter = SnowmedConverter()
        # basically we loop through the diagnoses, convert them to HCCs and risk scores, and then sum up the risk scores
        for enc in self.list_of_diag:
            if enc[1] <= starting_year:
                for diag in enc[2]:
                    HCC = converter.to_hcc(diag[0])
                    if HCC[0] not in already_added_hccs:
                        already_added_hccs.append(HCC[0])  # This makes sure we don't count an HCC more than once
                        risk_score = risk_score + HCC[2]
        return risk_score

    @staticmethod
    def init_from_fhir_patient_resource(resource):
        """Initialize a patient object from a FHIR Patient Resource record.
        
        Args:
            resource: a FHIR Patient Resource

        Returns:
            Entities.Patient
        """
        patient = Patient(int(resource['id']), '', '', '', '', date.today().year - 4)

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

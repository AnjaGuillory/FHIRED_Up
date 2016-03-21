import json
import urllib2
from datetime import datetime
from fhired import Entities


# Basic Process Flow
#
# 1.  Pull all of a members encounter IDs and encounter start dates by member ID
# 2.  Pull all snowmed codes by most encounter ID
# 3.  For each snowmed code, take only the record with the most recent service date


class FHIRQueries:
    ENCOUNTERS_BY_PATIENT = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Encounter?patient='
    CONDITION_BY_ENCOUNTER = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Condition?encounter='
    PATIENT_ID_BY_NAME = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Patient?name='
    
    
    
    # These are the get queries I use to access the GaTech FHIR server
    def __init__(self):
        pass

        
        
        
        

        
        
        
    def get_encounter_list(self, patient_id):
        """Submits a patient_id to the FHIR Server and returns a list containing
           the patient's encounter IDs and the start dates of the encounters
           :param patient_id: """
        encounter_list = []
        encounter_data = json.load(urllib2.urlopen(self.ENCOUNTERS_BY_PATIENT + str(patient_id)))
        for enc in encounter_data['entry']:
            encounter_list.append((enc['resource']['id'], int(enc['resource']['period']['start'][:4])))
        return encounter_list

    def get_condition_list(self, encounter_id):
        """Submits a encounter_id to the FHIR Server and returns a list containing
           the patient's conditions that were recorded at that encounter
           :param encounter_id: """
        try:
            condition_list = []
            condition_data = json.load(urllib2.urlopen(self.CONDITION_BY_ENCOUNTER + str(encounter_id)))
            for cond in condition_data['entry'][0]['resource']['code']['coding']:
                condition_list.append((cond['code'], cond['display'], cond['system']))
            return condition_list
        except:
            return []

    def get_all_patients_conditions(self, patient_id):
        """ Loops over all of a patients encounters, creating a full
            list of that patient's conditions.

            The output of this query is a list:
            [EncounterID, EncounterServiceYear, [list of [ConditionCode, ConditionName, ConditionCodingSystem]]]
            """
        try:
            all_patients_conditions = []
            encounters = self.get_encounter_list(patient_id)
            for enc in encounters:
                x = self.get_condition_list(enc[0])
                all_patients_conditions.append((enc[0], enc[1], x))
            return all_patients_conditions
        except:
            return []

            
            
        
    def get_patient_id_by_name(self, patient_name):
        '''submits a name to the FHIR server andf gets all the patient IDs that have that name'''
        patient_ID_list = []
        patient_ID_data = json.load(urllib2.urlopen(self.PATIENT_ID_BY_NAME + str(patient_name)))
        for patient in patient_ID_list['entry']:
            patient_ID_list.append(patient['resource']['id'])
        return encounter_list                    
            
            
            
            
            
            
            
            
            
    def get_patient_for(self, query):
        # TODO: make actual request
        pt1 = Entities.Patient(1, "Test Patient 1", "1/1/2000", "Female", "Near by", [])
        pt2 = Entities.Patient(1, "Test Patient 2", "1/1/2005", "Female", "Close", [])
        pt3 = Entities.Patient(1, "Test Patient 3", "1/1/1988", "Male", "Far far away", [])
        # TODO: make actual request
        return list([pt1, pt2, pt3])

    def get_patient_by_id(self, patient_id):
        patients = self.get_patient_for("Query")
        for patient in patients:
            if str(patient.pt_id) == patient_id:
                return patient

        return None

    def get_analysis_data(self, patient_id):
        # TODO: make actual request
        data = {'current_risk_score' : 20, 'candidate_risk_score' : 30 }
         # TODO: make actual request
        return data

    def get_candidate_hcc_for(self, patient_id):
        # TODO: make actual request
        chcc1 = Entities.CandidateHcc("123", "Name 1", 20)
        chcc2 = Entities.CandidateHcc("456", "Name 2", 20)
        chcc3 = Entities.CandidateHcc("78", "Name 3", 20)
        chcc4 = Entities.CandidateHcc("901", "Name 4", 20)
        # TODO: make actual request
        return list([chcc1, chcc2, chcc3, chcc4])

    def add_hcc_candidate_hcc_for(self, patient_id, hcc):
        # TODO
        pass

    def reject_hcc_candidate_hcc_for(self, patient_id, hcc):
        # TODO
        pass

    def view_hcc_candidate_hcc_for(self, patient_id, hcc):
        # TODO
        pass



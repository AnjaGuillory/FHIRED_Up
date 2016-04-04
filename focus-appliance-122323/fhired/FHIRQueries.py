import json
import urllib2
import urllib
from datetime import datetime, date

from google.appengine.api import memcache

import Entities


# Basic Process Flow
#
# 1.  Pull all of a members encounter IDs and encounter start dates by member ID
# 2.  Pull all snowmed codes by most encounter ID
# 3.  For each snowmed code, take only the record with the most recent service date

class FHIRQueries:
    ENCOUNTERS_BY_PATIENT = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Encounter?patient='
    CONDITION_BY_ENCOUNTER = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Condition?encounter='
    PATIENT_ID_BY_NAME = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Patient?name='
    PATIENT_RESOURCE = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Patient?'

    @staticmethod
    def get_cache_or_request(request):
        cached_result = memcache.get(request)
        if cached_result is not None:
            return cached_result
        remote_result = json.load(urllib2.urlopen(request))
        memcache.add(request, remote_result)
        return remote_result

    # # # These are the get queries I use to access the GaTech FHIR server
    def __init__(self):
        pass

    def get_encounter_list(self, patient_id):
        """Submits a patient_id to the FHIR Server and returns a list containing
           the patient's encounter IDs and the start dates of the encounters
           :param patient_id: """
        encounter_list = []
        encounter_data = FHIRQueries.get_cache_or_request(self.ENCOUNTERS_BY_PATIENT + str(patient_id))
        for enc in encounter_data['entry']:
            encounter_list.append((enc['resource']['id'], int(enc['resource']['period']['start'][:4])))
        return encounter_list

    def get_condition_list(self, encounter_id):
        """Submits a encounter_id to the FHIR Server and returns a list containing
           the patient's conditions that were recorded at that encounter
           :param encounter_id: """
        try:
            condition_list = []
            condition_data = FHIRQueries.get_cache_or_request(self.CONDITION_BY_ENCOUNTER + str(encounter_id))
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
        patient_ID_data = FHIRQueries.get_cache_or_request(self.PATIENT_ID_BY_NAME + str(patient_name))
        if int(patient_ID_data['total']):
            for patient in patient_ID_list['entry']:
                patient_ID_list.append(patient['resource']['id'])
        return patient_ID_list

    def get_patient_for(self, query, count=10):
        """Returns a list of matching patients give the provided query.

        Args:
            query (dictionary):  Valid keys: _id, name, given, birthdate, gender,  (for details: http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/resource?serverId=gatechrealease&resource=Patient)
            count (int): Number matching patient records to retrieve.  Default is 10.  (note: the "_count" paremeter will be added to "query" dictionary.)

        Returns:
            list[Entities.Patient]:  List of matching patient records.
        """

        # TODO: Add support for paging
        # TODO: need to return totalMatches

        patient_list = []

        # add "_count" attribute if not included to restrict number of matches returned.
        if not '_count' in query: query['_count'] = count

        patient_ID_data = FHIRQueries.get_cache_or_request(self.PATIENT_RESOURCE + urllib.urlencode(query))

        # get total number of matching patients.
        totalMatches = int(patient_ID_data['total'])

        if totalMatches > 0:
            for patient in patient_ID_data['entry']:
                patient_list.append(Entities.Patient.init_from_fhir_patient_resource(patient['resource']))

        return patient_list #, totalMatches

    def get_patient_by_id(self, patient_id):

        # build list of querystring params passed to the FHIR server.
        query = {'_id': patient_id}

        patients = self.get_patient_for(query)
        for patient in patients:
            if str(patient.pt_id) == patient_id:
                return patient

        return None

    def get_current_hccs_for(self, patient_id):
        # TODO: make actual request
        chcc1 = Entities.Hcc("123", date.today(),"Name 1", 20, "note 1")
        chcc2 = Entities.Hcc("456", date.today(), "Name 2", 20, "note 2")
        chcc3 = Entities.Hcc("78", date.today(), "Name 3", 20, "note 3")
        chcc4 = Entities.Hcc("901", date.today(), "Name 4", 20, "note 4")
        # TODO: make actual request

        return list([chcc1, chcc2, chcc3, chcc4])

    def get_candidate_hccs_for(self, patient_id, years, include_rejected):
        # TODO: make actual request
        chcc1 = Entities.Hcc("123",  date.today(), "Name 1", 20, "note 1")
        chcc2 = Entities.Hcc("456",  date.today(), "Name 2", 20, "note 2")
        chcc3 = Entities.Hcc("78",  date.today(), "Name 3", 20, "note 3")
        chcc4 = Entities.Hcc("901",  date.today(), "Name 4", 20, "note 4")

        """if years == 1 and not include_rejected:  # testing params
            return list([chcc1, chcc3, chcc4])

        if include_rejected:  # testing params
            return list([chcc1, chcc2, chcc3, chcc4, chcc1, chcc2, chcc3, chcc4, chcc1, chcc2, chcc3, chcc4])

        # TODO: make actual request
        return list([chcc1, chcc2, chcc3, chcc4])"""

    def add_hcc_candidate_hcc_for(self, patient_id, hcc):
        """ Add candidate hcc to patient list of hccs """
        patient = get_patient_by_id(patient_id)
        patient.list_of_diag.append(hcc)
        patient.list_of_cand_hccs(remove)
        pass

    def reject_hcc_candidate_hcc_for(self, patient_id, hcc):
        """ Remove candidate hcc from patient candidate hcc list"""
        patient = get_patient_by_id(patient_id)
        patient.list_of_diag.remove(hcc)
        pass

    def view_hcc_candidate_hcc_for(self, patient_id, hcc):
        """ View a specific hcc within the patient candidate hcc list"""
        patient = get_patient_by_id(patient_id)
        cand_hccs = patient.list_of_cand_hccs
        if hcc in cand_hccs:
            for elem in cand_hccs:
                if elem is hcc:
                    return elem
        return None        

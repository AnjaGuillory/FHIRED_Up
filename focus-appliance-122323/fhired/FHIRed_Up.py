from LookupTables import *
from FHIRQueries import *
from Snowmed_Mapping import ConvertSnowmedToHCC


class FHIRedUp:

    def __init__(self):
        self.queries = FHIRQueries()


    def get_hccs_by_time_period(self, patient_id, current_year):
        """

        :param patient_id:
        :param current_year:
        :return:
        """
        current_year_hccs = []
        historical_hccs = []

        # The format of the condition list is:
        # [EncounterID, EncounterServiceYear, [list of [ConditionCode, ConditionName, ConditionCodingSystem]]]

        # get all the patients encounters and the conditions reported at that encounter
        encounters = self.queries.get_all_patients_conditions(patient_id)

        # Loop over all the encounters
        for Enc in encounters:
            # loop over all the conditions in the encounter
            for Cond in Enc[2]:
                # One of our assumptions was that the GaTech FHIR server stored
                # diagnosis data using ICD9 codes.  This assumption was wrong.
                # Since the FHIR server uses SNOMED codes to store clinical information
                # we developed a lookup tables to convert SNOMED codes to ICD9
                # codes. 
                # diagnosis_code = a tuple containing HCC, HCC description and Risk Score
                diagnosis_code = ConvertSnowmedToHCC(Cond[0])

                if Enc[1] == current_year:
                    current_year_hccs.append(diagnosis_code)
                elif Enc[1] < current_year:
                    historical_hccs.append(diagnosis_code)

        current_year_hccs = set(current_year_hccs)
        historical_hccs = set(historical_hccs)

        return list(current_year_hccs), list(historical_hccs)

    def find_missing_diagnoses(self, current_year_hccs, historical_hccs):
        # Create a list storing only Historical HCCs missing from the current year
        missing_hccs = []
        for x in historical_hccs:
            if x not in current_year_hccs:
                missing_hccs.append(x)
        return missing_hccs

    def find_missing_diagnoses_by_patient_id(self, patient_id, current_year):
        """This is the most important piece of code - it take a patient number and year, and
            returns all of that patients missing diagnoses
            :param current_year:
            :param patient_id: """
        return self.find_missing_diagnoses(self.get_hccs_by_time_period(patient_id, current_year)[0], self.get_hccs_by_time_period(patient_id, current_year)[1])

    def add_diagnosis_to_current(self, missing_diagnoses, current_year_hccs, *hccs):
        """Takes variable input HCC for the corresponding diagnoses for addition,
            generated list of missing diagnoses, and the current list of diagnoses,
            returns new list for the current year including desired additions
            :param hcc:
            :param missing_diagnoses:
            :param current_year_hccs:"""
        for hcc in hccs:
            for pair in missing_diagnoses:
                if hcc == int(pair[0]):
                    current_year_hccs.append(pair)
                    break
        return current_year_hccs


    def remove_diagnosis_to_current(self, current_year_hccs, *hccs):
        """Takes variable input HCC for the corresponding diagnoses for addition,
            and the current list of diagnoses,
            returns new list for the current year without chosen diagnoses as desired
            :param hccs:
            :param current_year_hccs:"""
        for hcc in hccs:
            for pair in current_year_hccs:
                if hcc == int(pair[0]):
                    current_year_hccs.remove(pair)
                    break
        return current_year_hccs
        
    def add_patient_to_provider(self, patient_id):
        """Adds a patient to the list of patients under the provider's care"""
        patient = get_patient_by_id(patient_id)
        patientInfo = Entities.Patient(patient_id, patient.name , patient.dob, patient.gender, patient.address, patient.listOfDig)
        self.listOfPatients.append(patientInfo)








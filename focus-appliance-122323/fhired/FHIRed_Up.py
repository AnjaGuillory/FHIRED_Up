from LookupTables import *
from FHIRQueries import *


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
                # we developed code an lookup tables to convert SNOMED codes to ICD9
                # codes.  After extensive testing, we were unable to develop code that
                # could perform this very complicated mapping accurately.
                # So we decided to return SNOMED data to the end user, instead of
                # returning ICD9s or HCCs.
                #
                # This is the code we would have used if we could have got the
                # mapping to work.  Our problem was that a one-to-one mapping between
                # these two coding systems simply doesn't exist.
                #
                # This is what the original solution would have been:
                # DiagnosisCode = snowmed_to_hcc(Cond[0])
                #
                # This is the work-around code:
                diagnosis_code = (Cond[0], Cond[1])

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

    def add_diagnosis_to_current(self, hcc, missing_diagnoses, current_year_hccs):
        """Takes variable HCC for the corresponding diagnoses for addition,
            generated list of missing diagnoses, and the current list of diagnoses,
            returns new list for the current year including desired additions
            :param hcc:
            :param missing_diagnoses:
            :param current_year_hccs:"""
        for hcc in hccs:
            for code,diag in missing_diagnoses:
                if code is hcc:
                    current_year_hccs.append((code,diag))
                    break
            return current_year_hccs    
    def remove_diagnosis_to_current(self, *hccs, current_year_hccs):
        """Takes variable input HCC for the corresponding diagnoses for addition,
            and the current list of diagnoses,
            returns new list for the current year without chosen diagnoses as desired
            :param hccs:
            :param current_year_hccs:"""
        for hcc in hccs:
            for code,diag in missing_diagnoses:
                if code is hcc:
                    current_year_hccs.remove((code,diag))
                    break
            return current_year_hccs








from fhired import *
import Entities
from datetime import date
from LookupTables import LookupTables
from SnowmedConverter import SnowmedConverter
from FHIRQueries import FHIRQueries


class FHIRedUp():
    def __init__(self):
        # self.listOfPatients = list()
        self.queries = FHIRQueries()
        self.snowmed_converter = SnowmedConverter()

    def get_hccs(self, patient_id, current_year, max_past_years=None):
        """

        :type max_past_years: int
        :param patient_id:
        :param current_year:
        :return:
        """
        current_year_hccs = []
        historical_hccs = []
        if max_past_years is None:
            max_past_years = current_year - 5

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
                diagnosis_code = self.snowmed_converter.to_hcc(Cond[0])
                if diagnosis_code is not None:
                    hcc = Entities.Hcc(diagnosis_code[0], Enc[1], diagnosis_code[1], diagnosis_code[2], "")

                    if Enc[1] == current_year:
                        current_year_hccs.append(hcc)
                    elif current_year > Enc[1] > max_past_years:
                        historical_hccs.append(hcc)

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
        current_year_hccs, history_hccs = self.get_hccs(patient_id, current_year)
        return self.find_missing_diagnoses(current_year_hccs, history_hccs)

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

    def add_patient_to_provider(self, patient_id, current_year):  # we don't have providers yet.
        # """Adds a patient to the list of patients under the provider's care"""
        # patient = self.queries.get_patient_by_id(patient_id)
        # patient_info = Entities.Patient(patient_id, patient.name, patient.dob, patient.gender, patient.address, current_year)
        # self.listOfPatients.append(patient_info)
        pass

    def get_current_risk_score_for_pt(self, patient_id, include_selected):
        patient = self.queries.get_patient_by_id(patient_id)
        # I don't think we want to change this value when the include selected button is clicked
        # if include_selected:  # Todo Calculate proper score
        return patient.risk_score

    def get_candidate_risk_score_for_pt(self, patient_id, include_selected, current_year):
        # Risk score for the patient's current year
        look_up = LookupTables()
        risk_value = 0
        current_year_hccs, history_hccs = self.get_hccs(patient_id, current_year)

        for hcc_by_time in current_year_hccs:
            risk_value += look_up.hcc_to_risk_score_value(hcc_by_time)

        if include_selected:
            # add on the value for the "missing" HCCs
            missing_diag = self.find_missing_diagnoses(current_year_hccs, history_hccs)

            risk_value = risk_value + sum(look_up.hcc_to_risk_score_value(missing_diag))
        return risk_value

    def risks_scores_distribution(self, patient_id, include_selected):
        # all the entries must sum to 100
        if include_selected:  # testing_params
            entry_1 = Entities.RiskDistribution('Value 1', 56.33).for_chart()
            entry_2 = Entities.RiskDistribution('Value 2', 24.03).for_chart()
            entry_3 = Entities.RiskDistribution('Value 3', 10.38).for_chart()
            entry_4 = Entities.RiskDistribution('Value 4', 4.77).for_chart()
        else:
            entry_1 = Entities.RiskDistribution('Value 4', 5.77).for_chart()
            entry_2 = Entities.RiskDistribution('Value 2', 44.03).for_chart()
            entry_3 = Entities.RiskDistribution('Value 1', 16.33).for_chart()
            entry_4 = Entities.RiskDistribution('Value 3', 20.38).for_chart()

        return list([entry_1, entry_2, entry_3, entry_4])

    def risks_scores_list(self, patient_id, include_selected):
        # all the entries does not need must sum to 100
        if include_selected:  # testing_params
            entry_1 = Entities.RiskDistribution('Value 1', 56.33)
            entry_2 = Entities.RiskDistribution('Value 2', 24.03)
            entry_3 = Entities.RiskDistribution('Value 3', 10.38)
            entry_4 = Entities.RiskDistribution('Value 4', 4.37)
            entry_5 = Entities.RiskDistribution('Value 5', 3.27)
            entry_6 = Entities.RiskDistribution('Value 6', 6.77)
            entry_7 = Entities.RiskDistribution('Value 7', 7.47)
        else:
            entry_1 = Entities.RiskDistribution('Value 3', 20.38)
            entry_2 = Entities.RiskDistribution('Value 2', 34.03)
            entry_3 = Entities.RiskDistribution('Value 1', 46.33)
            entry_4 = Entities.RiskDistribution('Value 7', 5.47)
            entry_5 = Entities.RiskDistribution('Value 5', 1.27)
            entry_6 = Entities.RiskDistribution('Value 4', 14.37)
            entry_7 = Entities.RiskDistribution('Value 6', 2.77)

        return list([entry_1, entry_2, entry_3, entry_4, entry_5, entry_6, entry_7])

    def get_current_hccs_for(self, patient_id):
        current_year = Entities.get_current_year()
        current_year_hccs, _ = self.get_hccs(patient_id, current_year)
        return current_year_hccs

    # Candidate = History for now, waiting on spiro
    def get_candidate_hccs_for(self, patient_id, max_past_years, include_rejected):
        current_year = Entities.get_current_year()
        _, history_hccs = self.get_hccs(patient_id, current_year, max_past_years)
        return history_hccs

    def add_hcc_candidate_hcc_for(self, patient_id, hcc):  # Waiting for a proper implementation of a candidate list.
        """ Add candidate hcc to patient list of hccs """
        # patient = self.queries.get_patient_by_id(patient_id)
        # patient.list_of_diag.append(hcc)
        # patient.list_of_cand_hccs(remove)
        pass

    def reject_hcc_candidate_hcc_for(self, patient_id, hcc):
        """ Remove candidate hcc from patient candidate hcc list"""
        # patient = self.queries.get_patient_by_id(patient_id)
        # patient.list_of_diag.remove(hcc)
        pass

    def view_hcc_candidate_hcc_for(self, patient_id, hcc):
        """ View a specific hcc within the patient candidate hcc list"""
        patient = self.queries.get_patient_by_id(patient_id)
        # cand_hccs = patient.list_of_candidate_hccs
        # if hcc in cand_hccs:
        #     for elem in cand_hccs:
        #         if elem is hcc:
        #             return elem
        # return None
        pass

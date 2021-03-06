from fhired import *
import Entities
from datetime import date
from LookupTables import LookupTables
from SnowmedConverter import SnowmedConverter
from FHIRQueries import FHIRQueries
from google.appengine.api import memcache

from fhired.CurrentHcc import CurrentHcc


class FHIRedUp():
    def __init__(self):
        self.queries = FHIRQueries()
        self.snowmed_converter = SnowmedConverter()

    def get_patient_by_id(self, pt_id):
        key = 'pt-{0}'.format(str(pt_id))
        patient = memcache.get(key)
        if patient is not None:
            return patient

        patient = self.queries.get_patient_by_id(pt_id)
        memcache.add(key, patient)
        return patient

    def get_hccs(self, pt_id, current_year, max_past_years=None):
        """

        :type max_past_years: int
        :param pt_id:
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
        encounters = self.queries.get_all_patients_conditions(pt_id)

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
                    hcc = Entities.Hcc(int(diagnosis_code[0]), Enc[1], diagnosis_code[1], diagnosis_code[2], "")

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

    def find_missing_diagnoses_by_patient_id(self, pt_id, current_year):
        """This is the most important piece of code - it take a patient number and year, and
            returns all of that patients missing diagnoses
            :param current_year:
            :param patient_id: """
        current_year_hccs, history_hccs = self.get_hccs(pt_id, current_year)
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

    def add_patient_to_provider(self, pt_id, current_year):  # we don't have providers yet.
        # """Adds a patient to the list of patients under the provider's care"""
        # patient = self.queries.get_patient_by_id(patient_id)
        # patient_info = Entities.Patient(pt_id, patient.name, patient.dob, patient.gender, patient.address, current_year)
        # self.list_of_patients.append(patient_info)
        pass

    def get_current_risk_score_for_pt(self, pt_id, include_rejected):
        risk_score = 0
        current_hccs = self.get_current_hccs_for(pt_id, include_rejected)
        for current_hcc in current_hccs:
            risk_score += current_hcc.get_hcc().risk_score

        return risk_score

    def get_candidate_risk_score_for_pt(self, pt_id, include_rejected, year):
        # Risk score for the patient's current year
        # look_up = LookupTables()
        # risk_value = 0
        # current_year_hccs, history_hccs = self.get_hccs(pt_id, current_year)
        #
        # for hcc_by_time in current_year_hccs:
        #     risk_value += look_up.hcc_to_risk_score_value(hcc_by_time)
        #
        # if include_selected:
        #     # add on the value for the "missing" HCCs
        #     missing_diag = self.find_missing_diagnoses(current_year_hccs, history_hccs)
        #     for missing in missing_diag:
        #         missing_risk = look_up.hcc_to_risk_score_value(missing)
        #         risk_value = risk_value + missing_risk
        risk_value = 0
        for hcc in self.get_candidate_hccs_for(pt_id, year, include_rejected):
            risk_value += hcc.risk_score

        return risk_value

    def risks_scores_distribution(self, pt_id, year, include_rejected, include_candidate):
        hccs = self.get_current_hccs_for(pt_id, include_rejected)
        score_lists = list()
        for hcc_details in hccs:
            hcc = hcc_details.get_hcc()
            score_lists.append(Entities.RiskDistribution(hcc.name, hcc.risk_score, False).for_chart())

        if include_candidate:
            candidate_hccs = self.get_candidate_hccs_for(pt_id, year, include_rejected)
            for candidate_hcc in candidate_hccs:
                score_lists.append(Entities.RiskDistribution(candidate_hcc.name, candidate_hcc.risk_score, True).for_chart())

        return score_lists

    def risks_scores_list(self, pt_id, year, include_rejected, include_candidate):
        hccs = self.get_current_hccs_for(pt_id, include_rejected)
        score_lists = list()
        for hcc_details in hccs:
            hcc = hcc_details.get_hcc()
            score_lists.append(Entities.RiskDistribution(hcc.name, hcc.risk_score, False))

        if include_candidate:
            candidate_hccs = self.get_candidate_hccs_for(pt_id, year, include_rejected)
            for candidate_hcc in candidate_hccs:
                score_lists.append(Entities.RiskDistribution(candidate_hcc.name, candidate_hcc.risk_score, True))

        return score_lists

    def set_current_year_hccs_for(self, pt_id):
        if not CurrentHcc.exits(pt_id, None):
            current_year = Entities.get_current_year()
            current_year_hccs, _ = self.get_hccs(pt_id, current_year)
            for hcc in current_year_hccs:
                snow_meds = self.get_snow_meds_for(hcc.code)
                self.add_hcc_candidate_for(pt_id, hcc.code, snow_meds, "", "confirm")

    def get_current_hccs_for(self, patient_id, include_rejected):
        self.set_current_year_hccs_for(patient_id) # check if the new pt is missing hcc and adds it
        return CurrentHcc.get_all_by("pt_id", patient_id, include_rejected)

    def get_candidate_hccs_for(self, pt_id, max_past_years, include_rejected):
        current_year = Entities.get_current_year()
        store_current_year_hccs = [x.hcc for x in self.get_current_hccs_for(pt_id, not include_rejected)]
        current_year_hccs, historic_hccs = self.get_hccs(pt_id, current_year, max_past_years)
        hccs = list()

        for hcc in current_year_hccs+historic_hccs:
            if hcc.code not in store_current_year_hccs:
                hccs.append(hcc)

        return hccs


    def add_hcc_candidate_for(self, pt_id, hcc, snow_meds, notes, status):
        """ Add candidate hcc to patient list of hccs """

        if CurrentHcc.exits(pt_id, hcc):
            self.delete_hcc_for(pt_id, hcc)

        if snow_meds is not None:
            snow_meds = [str(x) for x in snow_meds]

        currentHcc = CurrentHcc(pt_id=pt_id,
                                hcc=hcc, status=status,
                                snow_med_codes=snow_meds, notes=notes)
        currentHcc.put()
        return currentHcc

    def delete_hcc_for(self, pt_id, hcc):
        if CurrentHcc.exits(pt_id, hcc):
            return CurrentHcc.delete_by(pt_id, hcc)

        return False

    def view_current_hcc_for(self, pt_id, hcc):
        if CurrentHcc.exits(pt_id, hcc):
            return CurrentHcc.get_by(pt_id, hcc)
        else:
            return CurrentHcc.empty(pt_id, hcc, [str(x) for x in self.get_snow_meds_for(hcc)])


    def get_snow_meds_for(self, hcc):
        return self.snowmed_converter.from_hcc(hcc)

    def save_hcc_candidate_for(self, pt_id, hcc, snow_meds, notes, status):
        if snow_meds is not None:
            snow_meds = [str(x) for x in snow_meds]

        currentHcc = CurrentHcc.get_by(pt_id, hcc)
        currentHcc.snow_med_codes = snow_meds
        currentHcc.status = status
        currentHcc.notes = notes
        currentHcc.save()
        return currentHcc

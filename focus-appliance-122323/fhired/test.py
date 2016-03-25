from FHIRQueries import *
from FHIRed_Up import *
from LookupTables import *
import pprint


def testing():
    tables = LookupTables()
    output = []
    output.append("Testing LookUp Table")
    output.append("")
    output.append("")
    output.append("")
    # code to test the dictionaries and the snowmed_to_hcc function

    assert tables.icd9_to_hcc('037') == 'TETANUS'
    assert tables.hcc_to_risk_score(181) == 'Chemotherapy'
    assert tables.hcc_to_risk_score_value(164) == 4.42
    assert tables.snowmed_to_icd9(422088007) == '648.80'
    assert tables.snowmed_to_hcc(422088007) == (147, 'ABN GLUCOSE IN PREG-UNSP')
    assert tables.snowmed_to_hcc(155855008) is None

    output.append('Tests all passed!')

    output.append("Testing FHIR Queries")
    output.append("")
    output.append("")
    output.append("")
    fhir_queries = FHIRQueries()
    ############### FOR TESTING ##################################################
    patient_id = '4'
    #encounters = get_encounter_list(patient_id)
    #pprint.pprint(encounters)

    #conditions = get_condition_list('129')
    #pprint.pprint(conditions)

    patients_conditions = fhir_queries.get_all_patients_conditions(patient_id)
    output.append(pprint.pformat(patients_conditions))
    output.append("Testing FHIRed UP")
    output.append("")
    output.append("")
    output.append("")
    fhir_ed_up = FHIRedUp()

    patient_id = 4
    current_year = 2010

    current_year_hccs = fhir_ed_up.get_hccs_by_time_period(patient_id, current_year)[0]
    HistoricalHCCs = fhir_ed_up.get_hccs_by_time_period(patient_id, current_year)[1]

    output.append("Current Year HCCs:")
    output.append(pprint.pformat(current_year_hccs, indent=4))
    output.append("")
    output.append("Historical Years HCCs:")
    output.append(pprint.pformat(HistoricalHCCs))
    output.append("")
    output.append("Missing HCCs:")
    output.append(pprint.pformat(fhir_ed_up.find_missing_diagnoses(current_year_hccs, HistoricalHCCs), indent=4))
    output.append("")
    output.append("Missing HCCs - by patient and year version:")
    output.append(pprint.pformat(fhir_ed_up.find_missing_diagnoses_by_patient_id(patient_id, current_year), indent=4))
    output.append("")
    output.append("")
    output.append("")

    patient_id = 5
    current_year = 2010

    current_year_hccs = fhir_ed_up.get_hccs_by_time_period(patient_id, current_year)[0]
    HistoricalHCCs = fhir_ed_up.get_hccs_by_time_period(patient_id, current_year)[1]

    output.append("Current Year HCCs:")
    output.append(pprint.pformat(current_year_hccs, indent=4))
    output.append("")
    output.append("Historical Years HCCs:")
    output.append(pprint.pformat(HistoricalHCCs, indent=4))
    output.append("")
    output.append("Missing HCCs:")
    output.append(pprint.pformat(fhir_ed_up.find_missing_diagnoses(current_year_hccs, HistoricalHCCs), indent=4))
    output.append("")
    output.append("Missing HCCs - by patient and year version:")
    output.append(pprint.pformat(fhir_ed_up.find_missing_diagnoses_by_patient_id(patient_id, current_year), indent=4))
    output.append("")
    output.append("")
    output.append("")

    patient_id = 6
    current_year = 2010

    current_year_hccs = fhir_ed_up.get_hccs_by_time_period(patient_id, current_year)[0]
    HistoricalHCCs = fhir_ed_up.get_hccs_by_time_period(patient_id, current_year)[1]

    output.append("Current Year HCCs:")
    output.append(pprint.pformat(current_year_hccs, indent=4))
    output.append("")
    output.append("Historical Years HCCs:")
    output.append(pprint.pformat(HistoricalHCCs, indent=4))
    output.append("")
    output.append("Missing HCCs:")
    output.append(pprint.pformat(fhir_ed_up.find_missing_diagnoses(current_year_hccs, HistoricalHCCs), indent=4))
    output.append("")
    output.append("Missing HCCs - by patient and year version:")
    output.append(pprint.pformat(fhir_ed_up.find_missing_diagnoses_by_patient_id(patient_id, current_year), indent=4))
    output.append("")
    output.append("")
    output.append("")
    return output


############### FOR TESTING ##################################################
if __name__ == "__main__":

    tests = testing()
    for test in tests:
        print test

    #pprint.pprint(Encounters)

    #from Get_FHIR_Data import get_condition_list
    #print get_condition_list(237)



# Basic Process Flow
#
# 1.  Pull all of a members encounter IDs and encounter start dates by member ID
# 2.  Pull all snowmed codes by most encounter ID
# 3.  For each snowmed code, take only the record with the most recent service date


import json
import urllib2


# These are the get queries I use to access the GaTech FHIR server
ENCOUNTERS_BY_PATIENT = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Encounter?patient='
CONDITION_BY_ENCOUNTER = 'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Condition?encounter='









def Get_Encounter_List(PatientID):
    '''Submits a PatientID to the FHIR Server and returns a list containing
       the patient's encounter IDs and the start dates of the encounters '''
    Encounter_list = []
    Encounter_Data = json.load(urllib2.urlopen(ENCOUNTERS_BY_PATIENT+ str(PatientID)))
    for enc in Encounter_Data['entry']:
        Encounter_list.append((enc['resource']['id'],enc['resource']['period']['start']) )
    return Encounter_list



def Get_Condition_List(EncounterID):
    '''Submits a EncounterID to the FHIR Server and returns a list containing
       the patient's conditions that were recorded at that encounter.
       EncounterID should be the numeric encounter identifyer'''
    try:
        Condition_List = []
        Condition_Data = json.load(urllib2.urlopen(CONDITION_BY_ENCOUNTER+ str(EncounterID)))
        for cond in Condition_Data['entry'][0]['resource']['code']['coding']:
            Condition_List.append((cond['code'],cond['display'],cond['system']) )
        return Condition_List
    except:
        return []
        




def Get_All_Patients_Conditions(PatientID):
    ''' Loops over all of a patients encounters, creating a full
        list of that patient's conditions'''
    try:
        All_Patients_Conditions = []
        encounters = Get_Encounter_List(PatientID)
        for enc in encounters:
            x = Get_Condition_List(enc[0])
            All_Patients_Conditions.append((enc[0], enc[1], x))
        return All_Patients_Conditions
    except:
        return []






############### FOR TESTING ##################################################
if __name__ == "__main__":
    import pprint
    PatientID = 4

    #encounters = Get_Encounter_List(PatientID)
    #pprint.pprint(encounters)

    #conditions = Get_Condition_List('129')
    #pprint.pprint(conditions)

    output = Get_All_Patients_Conditions(PatientID)
    pprint.pprint(output)








    


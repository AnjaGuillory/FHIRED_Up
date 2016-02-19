from LookupTables import SNOWMED_to_HCC
from FHIRQueries import Get_All_Patients_Conditions




def GetHCCsByTimePeriod(PatientID, CurrentYear):
    CurrentYearHCCs  = []
    HistoricalHCCs = []



    # The format of the condition list is:
    # [EncounterID, EncounterServiceYear, [list of [ConditionCode, CoinditionName, ConditionCodingSystem]]]

    # get all the patients encounters and the conditions reported at that encounter
    Encounters = Get_All_Patients_Conditions(PatientID)


    # Loop over all the enounters
    for Enc in Encounters:
        # loop over all the contitions in the encounter
        for Cond in Enc[2]:


            # TODO: for testing purposes, I'm using snomed code.
            # I need to get the conversion software working correctly
            ICD9 = (Cond[0], Cond[1])
            #ICD9 = SNOWMED_to_HCC(Cond[0])


            if Enc[1] == CurrentYear:
                CurrentYearHCCs.append(ICD9)
            elif Enc[1]<CurrentYear:
                HistoricalHCCs.append(ICD9)
                

    CurrentYearHCCs = set(CurrentYearHCCs)
    HistoricalHCCs = set(HistoricalHCCs)
    return (CurrentYearHCCs, HistoricalHCCs)


def Find_Missing_Diagnoses(CurrentYearHCCs, HistoricalHCCs):
    # Create a list storing only Historical HCCs missing from the current year
    Missing_HCCs = []
    for x in HistoricalHCCs:
        if x not in CurrentYearHCCs:
            Missing_HCCs.append(x)
    return Missing_HCCs





def FindMissingDiagnosesByPatientID(PatientID, CurrentYear):
    ''' This is the most important piece of code - it take a patient number and year, and
        returns all of that patients missing diagnoses'''
    return Find_Missing_Diagnoses(GetHCCsByTimePeriod(PatientID, CurrentYear)[0], GetHCCsByTimePeriod(PatientID, CurrentYear)[1])










############### FOR TESTING ##################################################
if __name__ == "__main__":


    import pprint

    PatientID = 5
    CurrentYear = 2010


    CurrentYearHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[0]
    HistoricalHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[1]


    print "Current Year HCCs:"
    pprint.pprint(CurrentYearHCCs)
    print ""
    print ""
    print "Historical Years HCCs:"
    pprint.pprint(HistoricalHCCs)
    print ""
    print "Missing HCCs:"
    pprint.pprint(Find_Missing_Diagnoses(CurrentYearHCCs, HistoricalHCCs))
    print ""
    print "Missing HCCs - by patient and year version:"
    pprint.pprint(FindMissingDiagnosesByPatientID(PatientID, CurrentYear))    



    #pprint.pprint(Encounters)

    #from Get_FHIR_Data import Get_Condition_List
    #print Get_Condition_List(237)




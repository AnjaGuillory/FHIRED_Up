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
            # One of our assumptions was that the GaTech FHIR server stored
            # diagnosis data using ICD9 codes.  This assumption was wrong.
            # Since the FHIR server uses SNOMED codes to store clinical infomation
            # we developed code an lookup tables to convert SNOMED codes to ICD9
            # codes.  After extensive testing, we were unable to develop code that
            # could perform this very complicated mapping accuratly.
            # So we decided to return SNOMED data to the end user, instead of
            # returning ICD9s or HCCs.
            #
            # This is the code we would have used if we could have got the
            # mapping to work.  Our problem was that a one-to-one mapping between
            # these two coding systems simply doesn't exist.
            #
            # This is what the original solution would have been:
            #DiagnosisCode = SNOWMED_to_HCC(Cond[0])
            #
            # This is the work-around code:
            DiagnosisCode = (Cond[0], Cond[1])


            if Enc[1] == CurrentYear:
                CurrentYearHCCs.append(DiagnosisCode)
            elif Enc[1]<CurrentYear:
                HistoricalHCCs.append(DiagnosisCode)
                

    CurrentYearHCCs = set(CurrentYearHCCs)
    HistoricalHCCs = set(HistoricalHCCs)
    return (list(CurrentYearHCCs), list(HistoricalHCCs))


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

    PatientID = 4
    CurrentYear = 2010


    CurrentYearHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[0]
    HistoricalHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[1]


    print "Current Year HCCs:"
    pprint.pprint(CurrentYearHCCs)
    print ""
    print "Historical Years HCCs:"
    pprint.pprint(HistoricalHCCs)
    print ""
    print "Missing HCCs:"
    pprint.pprint(Find_Missing_Diagnoses(CurrentYearHCCs, HistoricalHCCs))
    print ""
    print "Missing HCCs - by patient and year version:"
    pprint.pprint(FindMissingDiagnosesByPatientID(PatientID, CurrentYear))    
    print ""
    print ""
    print ""



    PatientID = 5
    CurrentYear = 2010


    CurrentYearHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[0]
    HistoricalHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[1]


    print "Current Year HCCs:"
    pprint.pprint(CurrentYearHCCs)
    print ""
    print "Historical Years HCCs:"
    pprint.pprint(HistoricalHCCs)
    print ""
    print "Missing HCCs:"
    pprint.pprint(Find_Missing_Diagnoses(CurrentYearHCCs, HistoricalHCCs))
    print ""
    print "Missing HCCs - by patient and year version:"
    pprint.pprint(FindMissingDiagnosesByPatientID(PatientID, CurrentYear))    
    print ""
    print ""
    print ""




    PatientID = 6
    CurrentYear = 2010


    CurrentYearHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[0]
    HistoricalHCCs = GetHCCsByTimePeriod(PatientID, CurrentYear)[1]


    print "Current Year HCCs:"
    pprint.pprint(CurrentYearHCCs)
    print ""
    print "Historical Years HCCs:"
    pprint.pprint(HistoricalHCCs)
    print ""
    print "Missing HCCs:"
    pprint.pprint(Find_Missing_Diagnoses(CurrentYearHCCs, HistoricalHCCs))
    print ""
    print "Missing HCCs - by patient and year version:"
    pprint.pprint(FindMissingDiagnosesByPatientID(PatientID, CurrentYear))    
    print ""
    print ""
    print ""




    #pprint.pprint(Encounters)

    #from Get_FHIR_Data import Get_Condition_List
    #print Get_Condition_List(237)




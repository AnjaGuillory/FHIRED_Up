from LookupTables import SNOWMED_to_HCC
from FHIRQueries import Get_All_Patients_Conditions


# for testing
import pprint


# For testing
PatientID = 5
CurrentYear = 2010


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
        else:
            HistoricalHCCs.append(ICD9)
            

CurrentYearHCCs = set(CurrentYearHCCs)
HistoricalHCCs = set(HistoricalHCCs)

# Create a list storing only Historical HCCs missing from the current year
Missing_HCCs = []
for x in HistoricalHCCs:
    if x not in CurrentYearHCCs:
        Missing_HCCs.append(x)





# For Testing

#pprint.pprint(Encounters)

print "Current Year HCCs:"
pprint.pprint(CurrentYearHCCs)
print ""
print ""
print "Historical Years HCCs:"
pprint.pprint(HistoricalHCCs)
print ""
print "Missing HCCs:"
pprint.pprint(Missing_HCCs)


#from Get_FHIR_Data import Get_Condition_List
#print Get_Condition_List(237)






############### FOR TESTING ##################################################
if __name__ == "__main__":
    pass

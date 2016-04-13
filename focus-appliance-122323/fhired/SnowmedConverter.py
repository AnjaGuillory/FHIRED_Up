# Converts snowmed code to ICD10, then ICD10 to ICD9, then ICD9 to Massachusetts HCCs and platinum risk scores.
from SnowmedDict import Snowmed_to_HCC_Dictionary

class SnowmedConverter:
    def __init__(self):
        pass

    @staticmethod
    def to_hcc(snowmedCode):
        try:
            code = Snowmed_to_HCC_Dictionary.get(str(snowmedCode))
            if code is not None:
                hcc = code[2]
                hccDescription = code[3]
                riskScore = code[4]
                if hcc=='NA' or hccDescription == 'NA':
                    return None
                else:
                    return (hcc, hccDescription, riskScore)
            return None
        except ValueError:
            print ValueError
            return None

    @staticmethod
    def from_hcc(hcc): #Slow :(, adding ticket
        try:
            snow_meds = list()
            for snow_med, code in Snowmed_to_HCC_Dictionary.iteritems():
                if code[2] is not None and code[2] == str(hcc):
                    hccDescription = code[3]
                    riskScore = code[4]
                    snow_meds.append((snow_med, hccDescription, riskScore))

            snow_meds.sort()
            return snow_meds
        except ValueError:
            print ValueError
            return None

    @staticmethod
    def get_hcc_details(hcc): #Slow :(, adding ticket
        try:
            for snow_med, code in Snowmed_to_HCC_Dictionary.iteritems():
                if code[2] is not None and code[2] == str(hcc):
                    hccDescription = code[3]
                    riskScore = code[4]
                    return (hcc, hccDescription, riskScore)
            return None
        except ValueError:
            print ValueError
            return None


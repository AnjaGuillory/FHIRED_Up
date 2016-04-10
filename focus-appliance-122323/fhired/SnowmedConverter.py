# Spiro Ganas
# 2/24/16
#
# Converts snowmed code to ICD10, then ICD10 to ICD9, then ICD9 to Massachusetts HCCs and platinum risk scores.
from SnowmedDict import Snowmed_to_HCC_Dictionary

class SnowmedConverter:
    def __init__(self):
        pass

    def to_hcc(self, snowmedCode):
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




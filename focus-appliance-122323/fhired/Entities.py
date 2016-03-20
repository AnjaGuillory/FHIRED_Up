
class Patient:
    def __init__(self, pt_id, name, dob, gender, address, listOfDiag):
        self.pt_id = pt_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.listOfDiag = listOfDiag
        
    
class Provider:
    def __init__(self, prov_id, name, listOfPatients):
        self.prov_id = prov_id
        self.name = name
        self.listOfPatients = listOfPatients


class CandidateHcc:
    def __init__(self, code, name, risk_score):
        self.code = code
        self.name = name
        self.risk_score = risk_score

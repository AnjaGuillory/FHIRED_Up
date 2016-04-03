import FHIRQueries



class Patient:

    def __init__(self, pt_id, name, dob, gender, address):
        self.pt_id = pt_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.list_of_diag = self.set_diagnoses_list()
        self.risk_score = self.cal_risk_score()

        
    def set_diagnoses_list(self):
        """Uses the patient ID to get the list of SNOMED
           codes for that patient's conditions from the FHIR server"""
        X=FHIRQueries
        # The output of this query is a list:
        # [EncounterID, EncounterServiceYear, [list of [ConditionCode, ConditionName, ConditionCodingSystem]]]
        self.list_of_diag = X.get_all_patients_conditions(self.pt_id)
        
        
    def cal_risk_score(self, current_year):
        '''Calculates the patient's risk score for the 
           year entered as a parameter'''
        riskScore = 0
        alreadyAddedHCCs = []
        # basically we loop through the diagnoses, convert them to HCCs and risk scores, and then sum up the risk scores
        For enc in self.list_of_diag:
            if enc[1] == current_year:
                for diag in enc[2]:
                    HCC = Snowmed_mapping.ConvertSnowmedToHCC(diag[0])
                    if HCC[0] not in alreadyAddedHCCs:
                       alreadyAddedHCCs.append(HCC[0])  #This makes sure we don't count an HCC more than once
                       riskScore = riskScore+HCC[2]
        return riskScore

    @staticmethod
    def init_from_fhir_patient_resource(resource):
        """Initialize a patient object from a FHIR Patient Resource record.
        
        Args:
            resource: a FHIR Patient Resource

        Returns:
            Entities.Patient
        """ 
        patient = Patient(int(resource['id']), '', '', '', '', [])
        
        if 'birthDate' in resource: patient.dob = resource.get('birthDate')
        if 'gender' in resource: patient.gender = resource.get('gender')

        # format the name           
        if 'name' in resource and len(resource['name']) > 0: 
            if 'given' in resource['name'][0]: patient.name = ' '.join(resource['name'][0].get('given')) 
            if 'family' in resource['name'][0]: patient.name += ' ' + ' '.join(resource['name'][0].get('family'))

        # format address (use "home" address only)
        address = {}
        if 'address' in resource:
            for a in resource['address']:
                if a.get('use') == 'home':
                    if 'line' in a: address['line'] = a.get('line')
                    if 'city' in a: address['city'] = a.get('city')
                    if 'state' in a: address['state'] = a.get('state')
                    if 'postalCode' in a: address['postalCode'] = a.get('postalCode')

                    break
        patient.address = address

        return patient




class Provider:
    def __init__(self, prov_id, name, list_of_patients):
        self.prov_id = prov_id
        self.name = name
        self.listOfPatients = list_of_patients


class Hcc:
    def __init__(self, code, date, name, risk_score, notes):
        self.code = code
        self.name = name
        self.date = date
        self.risk_score = risk_score
        self.notes = notes


class RiskDistribution:
    def __init__(self, name, risk_score):
        self.name = name
        self.risk_score = risk_score

    def for_chart(self):
        return {"name" : self.name, "y" : self.risk_score }

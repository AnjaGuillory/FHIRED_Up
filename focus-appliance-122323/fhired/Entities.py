
class Patient:



    def __init__(self, pt_id, name, dob, gender, address, listOfDiag):
        self.pt_id = pt_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.listOfDiag = listOfDiag
    


    @staticmethod
    def initFromFHIRPatientResource (resource):
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
        patient.name = ' '.join(resource['name'][0].get('given')) + ' ' + ' '.join(resource['name'][0].get('family'))

        # format address (use "home" address only)
        address = ''
        if 'address' in resource:
            for a in resource['address']:
                if a.get('use') == 'home':
                    #TODO: Line breaks <br /> may need to be replaced with a better newline indicator
                    if 'line' in a: address = ' '.join(a.get('line')) + '<br />'
                    if 'city' in a: address += a.get('city') + ', '                  
                    if 'state' in a: address += a.get('state') + ' '                
                    if 'postalCode' in a: address += a.get('postalCode')

                    break
        patient.address = address;

        return patient
                   
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

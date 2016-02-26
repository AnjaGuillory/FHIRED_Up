
####February 29, 2016
* Requirements Document approval
  * _Notes to review:_
    * **Codes** -- Are APCD codes still needed? Spiro: For #1,  we were able to create a mapping table to convert Snomed codes into the HCC categories used in the risk adjustment process.
    * **Database** -- Will we need a database (ex: MySQL or NoSQL) to persist any data outside of FHIR? Spiro: our lookup tables are small enough to store as python dictionaries, and the FHIR server lets us create/update records.  So we may be able to complete the project without a database.
    * **Authentication** -- Is this necessary for the scope of this application?  Should we at a minimum have a single hard-code username/password to access the tool since it'll be publicly available.
    * **Past HCCs** -- How many years back should we look for candidate HCCs?
    * **Application name** -- One proposal is "Risk Adjustment Data Validation (RADV)" (by FHIRed Up)
    * **Logging** -- Will we be able to log all activity (ex: confirmations, rejections) in a patient's EHR?
    * **Audit Trail by Doctor** -- An idea, time permitting, is to provide an audit trail of confirmations & rejections by a doctor.  Of course if we have only a single login into the system there'd effectively be just one doctor
    * **A few other nice-to-haves:
    ** •	The ability to compare an uploaded file containing APCD data to the FHIR data
    ** •	The ability to search all patients on the FHIR server and identify those with the most missing HCCs





* Progress
* Other issues

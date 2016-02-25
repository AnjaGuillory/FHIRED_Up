## Requirements Document
###ACA Risk Adjustment EHR Data Validation (RADV) Tool 
######by FHIRed Up
---

###1 User Requirements

####1.1 Software Components / Interfaces

* Python
* Web Browser (HTML5 compliant)
* Google Application Engine


####1.2 Data Sources
* Georgia Tech's FHIR Server
* Massachusetts APCD data dictionary
* ICD9, ICD10, SNOMED, MA APCD, & CMS HCC *(codes and descriptions)* with mappings between each.
* MySQL (or NoSQL) database for persisting login credentials, audit trail *(including doctor approvals & dismissals of candidate HCCs for a patient)*, etc.

####1.3 User Interfaces

* Users will access the tool via a browser interface.
* Users will login with a username/password challenge.
* Users will lookup a patient by patient id -or- patient name. 


####1.4 User Characteristics

* Users of this application will be nurses, doctors and other health care professionals responsible for entering patient HCC codes.

###2 System Requirements

####2.1 Functional Requirements

1. Program shall be named "Risk Adjustment Data Validation (RADV) (by FHIRed Up)".  
2. Program shall be written Python v2.7  
3. Ability to map codes between ICD9, ICD10, SNOMED, MA APCD, & CMS HCCs 
4. Ability to lookup a patient by their ID or Name.
5. Ability to extract HCC values from a patient's EHR and segment these by calendar year.
6. Ability to list HCC values present in a patient's prior calendar years that are not yet present in the current calendar year.
7. Ability to notify the doctor of HCC values listed in prior calendar years that are not present in the current calendar year (with the exception of any HCCs already excluded for the calendar year) *(see: 2.1.9)*.
7. Ability to notify the doctor that no HCC values listed in prior calendar years are missing in the current calendar year.
8. Ability for a doctor to approve one or more candidate missing HCCs *(identified in 2.1.6)* in the current calendar year should be added to the patient's EHR, along with notes for identified comorbidities.
9. Ability for a doctor to dismiss *(reject)* one or more candidate missing HCCs *(identified in 2.1.6)* be added to the patient's EHR for the remainder of the current calendar year, along with optional notes justifying the rejection. 
10. Rejected HCCs by a doctor should be excluded from the list of candidate HCCs for the given patient for the remainder of the current calendar year *(see: 2.1.6)*
11. Log all activity including notifications, confirmations, denials, etc. in an audit trail which includes current user ID, patient ID, and relevant metadata.
12. Provide an audit trail report of a patient's HCCs by calendar year and any approval or rejections of candidate HCCs
13. Provide an audit trail report by doctor of all approvals and rejections of candidate HCC's by patient.

####2.2 Non-Functional Requirements

1. Program should be browser agnostic though assume HTML5 compliance.
2. Error messages should be user-friendly and contain non-cryptic messages.
3. Program shall be capable of processing several thousand records per second on average. 
4. Notifications of candidate HCCs for a patient should include dates of HCCs (and other relevant information) from prior calendar years.
 
###3 Acronyms

* CMS - Centers for Medicare & Medicaid Services
* EHR - Electronic Health Record
* HCC - Hierarchical Condition Categories 
* ICD (9 & 10) - International Classification of Diseases (ninth & tenth revisions)
* ICD-9-CM - International Classification of Diseases,Ninth Revision, Clinical Modification (ICD-9-CM)
* MA APCD - Massachusetts All Payer Claims Database
* SNOMED - Systematized Nomenclature of Medicine

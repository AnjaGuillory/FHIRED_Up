## Requirements Document
###Risk Adjustment Data Validation (RADV) Tool 
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
* ICD9, ICD10, SNOMED, & CMS HCC *(codes and descriptions)* with mappings between each. 
* User.py will contain hardcoded user data and passwords in SHA256

####1.3 User Interfaces

* Users will access the tool via a browser interface.
* Users will login with a username/password challenge.
* Users will lookup a patient by patient id -or- patient name. 
* Users will be presented with candidate HCCs not present in data from current calendar but present in three prior calendar years. 
* Users will be able to select which candidate HCCs to add to the patient's EHR.
* Users will be able to select which candidate HCCs to reject for the remainder of the calendar year.  Notes will be added to the patient's EHR.

####1.4 User Characteristics

* Users of this application will be nurses and doctors responsible for entering patient HCC codes.

###2 System Requirements

####2.1 Functional Requirements

1. Program shall be named "Risk Adjustment Data Validation (RADV) (by FHIRed Up)".  
2. Program shall be written Python v2.7  
3. Ability to map codes between ICD9, ICD10, SNOMED, & CMS HCCs 
4. Ability to lookup a patient by their ID or Name.
5. Ability to extract HCC values from a patient's EHR and segment these by calendar year.
6. Ability to extract HCC values present in a patient's three prior calendar years that are not yet present in the current calendar year (with the exception of any HCCs already excluded for the calendar year) *(see: 2.1.10 and 2.1.11)*..
7. Ability to present the user (nurse or doctor) with a list of candidate HCC values from prior calendar years that are not present in the current calendar year (with the exception of any HCCs already excluded for the calendar year) *(see: 2.1.10 and 2.1.11)*.
8. Ability to present the user a note that no candidate HCC values listed in prior calendar years are missing in the current calendar year.
9. Ability for a doctor to confirm one or more candidate HCCs *(identified in 2.1.6)* in the current calendar year should be added to the patient's EHR, along with notes for identified comorbidities.
10. Ability for a doctor to reject one or more candidate  HCCs *(identified in 2.1.6)* to be added to the patient's EHR for the remainder of the current calendar year, along with optional notes justifying the rejection using codes from condition status (Provisional, refuted, entered-in-error, or unknown). 
11. Rejected HCCs by a doctor should be excluded from the list of candidate HCCs for the given patient for the remainder of the current calendar year *(see: 2.1.6)*
12. Log all activity including notifications, confirmations, denials, etc. in a patient's EHR audit trail 
13. Provide a filter for the patient's EHR audit trail by calendar year and HCC.
14. Provide an audit trail report by doctor of all approvals and rejections of candidate HCC's by patient. 
15. Provide traffic light icon based on total risk assessment of candidate HCCs to guide user when adding HCCs
16. Provide timeline to user of when a candidate HCC was previously on a patient's EHR.
17. Provide performance analytics of tool for rejected and candidate HCCs by perecent.

####2.2 Non-Functional Requirements

1. Program should be browser agnostic though assume HTML5 compliance.
2. Error messages should be user-friendly and contain non-cryptic messages.
3. Program shall be capable of processing several thousand records per second on average. 
4. Candidate HCCs for a patient should include dates of HCCs *(and other relevant information)* from prior calendar years.
5. Program should be written in a strongly typed language for security purposes.
6. All user inputs should be validated for data integrity & security.
 
###3 Acronyms

* CMS - Centers for Medicare & Medicaid Services
* EHR - Electronic Health Record
* HCC - Hierarchical Condition Categories 
* ICD (9 & 10) - International Classification of Diseases (ninth & tenth revisions)
* ICD-9-CM - International Classification of Diseases,Ninth Revision, Clinical Modification (ICD-9-CM)
* SNOMED - Systematized Nomenclature of Medicine

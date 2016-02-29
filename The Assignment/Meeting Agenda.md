
####February 29, 2016
* Requirements Document approval
  * _Notes to review:_
    * **Codes** -- Are APCD codes still needed? **Spiro** : For #1,  we were able to create a mapping table to convert Snomed codes into the HCC categories used in the risk adjustment process.
    * **Database** -- Will we need a database (ex: MySQL or NoSQL) to persist any data outside of FHIR? **Spiro**: our lookup tables are small enough to store as python dictionaries, and the FHIR server lets us create/update records.  So we may be able to complete the project without a database. **Dan**: :  if we do need to store data it provides a free API called Datastore which is a high-performance, distributed, NoSQL database with replication between data centers (I added sample code to the skeleton to demonstrate usage of it in Python).   
    * **Authentication** -- Is this necessary for the scope of this application?  Should we at a minimum have a single hard-code username/password to access the tool since it'll be publicly available. **Dan** " Flask provides authentication so I would imagine we just use the framework; of those provided options most likely basic as you suggesting with just log on credentials. **RohanTA** : this is not a core requirement. Hard coding a default username password is fine. **Augusto**: 1 - (Really Nice) Login system: Now we have users and session powered logins.
     the password and username and hard coded but the rest is good.
     you can add a user simply editing the file User.py, the password is in SHA256, you can calculate a password here, http://www.xorbin.com/tools/sha256-hash-calculator. 
The default user is FHIRedUp and password is PjV7kGTD

    * **Past HCCs** -- How many years back should we look for candidate HCCs?
    * **Application name** -- One proposal is "Risk Adjustment Data Validation (RADV)" (by FHIRed Up)
    * **Logging** -- Will we be able to log all activity (ex: confirmations, rejections) in a patient's EHR? **Dan**: Basic auditable logs are available from the platform (really any PaaS will have that built-in) without us writing any code so I think we can at least consider that a viable solution which is already finished ;)
- I can spend some time Monday showing some of these features and cover platform ops as well as code QA  **RohanTA**: Yes, a log would be useful to have. 
As for the audit trail, please let me rephrase what I said - maybe I wasn’t clear. If time permits - by all means have an audit trail - but instead of having a list or table, think about visualizing the data instead. It would make it much easier to follow. If you do this, visualize the data as a whole first, and then maybe you could have an add-on that deals exclusively with a physician. For example, a physician might have cases of missing risk with two different patients - one in 2007 and one in 2009. Your audit trail would show a timeline of sorts visualizing these “missing risk cases” instead of just listing them.


    * **Audit Trail by Doctor** -- An idea, time permitting, is to provide an audit trail of confirmations & rejections by a doctor.  Of course if we have only a single login into the system there'd effectively be just one doctor
    * **A few other nice-to-haves**:
    
        •	The ability to compare an uploaded file containing APCD data to the FHIR data. 

        •	The ability to search all patients on the FHIR server and identify those with the most missing HCCs.





* Progress
*  **Augusto**: 2 - Now we have a layout and a CSS framework to work with, 3- We can visualize a basic pt history on the dashboard, you can try with  pt_id  4, 5 etc. 

* Other issues

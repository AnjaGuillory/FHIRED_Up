def get_categories_for_risks(values):
    categories = []
    data_values = []
    for value in values:
        categories.append(value.name)
        data_values.append(value.risk_score)

    return categories, data_values

def risk_score_total(self, patient_id, include_selected, current_year):
        # Risk score for the patient's current year
        look_up = LookupTables()

        risk_value = 0
        for hcc_by_time in self.get_hccs_by_time_period(patient_id, current_year)[0]:
            risk_value += look_up.hcc_to_risk_score_value(hcc_by_time)

        if include_selected:
            # add on the value for the "missing" HCCs
            missing_diag = self.find_missing_diagnoses(self.get_hccs_by_time_period(patient_id, current_year)[0],
                                                       self.get_hccs_by_time_period(patient_id, current_year)[1])

            risk_value = risk_value + sum(look_up.hcc_to_risk_score_value(missing_diag))
        return risk_value

    def pie_chart_slice(risk_value, list([entry_1, entry_2, entry_3, entry_4, entry_5, entry_6, entry_7])):
        #to determine the percent that each slice of the pie represents. Each slice in the resulting list is the percentage for the entry
        slices=[]
        for pslice in list:
            pslice[0]=entry_[0]/risk_value
            slices.append(pslice)
        return slices
    def bar_chart_data(snowMed code):
        #need to edit variable so that it's the list of entries which will be referred to as bars, but I'm pulling from the Snowmed codes that spiro defined in his SnowmedConverter.py
        
        categories=[]
        values=[]
        for bar in bars:
            categories.append(hccDescription)
            values.append(riskScore)
        return [categories, values]
    
            
        
    
            

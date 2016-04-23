def get_categories_for_risks(values):
    categories = []
    current_values = []
    candidate_values = []
    for value in values:
        categories.append(value.name)
        if (value.is_candidate) :
            current_values.append(0)
            candidate_values.append(value.risk_score)
        else :
            current_values.append(value.risk_score)
            candidate_values.append(0)

    return categories, current_values, candidate_values

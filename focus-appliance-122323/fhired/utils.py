def get_categories_for_risks(values):
    categories = []
    data_values = []
    for value in values:
        categories.append(value.name)
        data_values.append(value.risk_score)

    return categories, data_values

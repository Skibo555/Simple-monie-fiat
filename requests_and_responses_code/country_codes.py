import json


def load_country_code():
    with open('CountryCodes.json', "r") as file:
        data = json.load(file)
    return data

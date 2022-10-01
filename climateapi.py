import requests

climate_url = 'https://beta3.api.climatiq.io/travel/flights'

climate_headers = {
    'content-type': 'application/json',
    'Authorization' : 'Bearer CKA1H24HQ5M1JBGK2EXP8C3EV865'}

departure_airport = 'JFK'
arrival_airport = 'SFO'

def get_carbon_emission(origin, destination):
    climate_data = {
        "legs": [
            {
                "from": origin,
                "to": destination,
                "passengers": 2,
                "class": "economy"
            },
            {
                "from": destination,
                "to": origin,
                "passengers": 2,
                "class": "economy"
            }
        ]
    }
    response = requests.post(url=climate_url, headers=climate_headers, json=climate_data)
    return(response.json().get("co2e"))
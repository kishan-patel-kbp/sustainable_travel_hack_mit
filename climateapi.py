import requests

climate_url = 'https://beta3.api.climatiq.io/travel/flights'

climate_headers = {
    'content-type': 'application/json',
    'Authorization' : 'Bearer CKA1H24HQ5M1JBGK2EXP8C3EV865'}

departure_airport = 'JFK'
arrival_airport = 'SFO'

climate_data = {
        "legs": [
            {
                "from": arrival_airport,
                "to": departure_airport,
                "passengers": 2,
                "class": "economy"
            },
            {
                "from": departure_airport,
                "to": arrival_airport,
                "passengers": 2,
                "class": "economy"
            }
        ]
    }

response = requests.post(url=climate_url, headers=climate_headers, json=climate_data)
print(response.json().get("co2e"))
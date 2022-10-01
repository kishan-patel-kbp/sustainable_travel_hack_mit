import requests

API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYmZkZGJhZTgwYjY3Y2MwMDM4NDZhYTFiYTYwMGU0NTExNDNiYWI0OGIxZjc1YzU4NDcyYTgxMTQ0YWVjZDA1MWRlNGJmYjE3ZGE2Yzk3MGIiLCJpYXQiOjE2NjQ2NDQ3NDQsIm5iZiI6MTY2NDY0NDc0NCwiZXhwIjoxNjk2MTgwNzQ0LCJzdWIiOiIxNDAzNCIsInNjb3BlcyI6W119.aSjVK0Q3SQ01ExN3WVxtXD5_LTR95zrWk-_rVuGhrAaU7CuhlnlWovTvWSh5URa4SHLeL4LN5nIqUhj3ZMcYoA"

adults = 1

departure_airport = 'PDX'

arrival_airport = 'EWR'

departure_date = '2022-10-16'

api_url = ("https://app.goflightlabs.com/search-all-flights?access_key=" + API_KEY + "&adults=1&origin=MAD&destination=FCO&departureDate=2022-10-06")



response = requests.get(api_url)

# print(response.text[0])
data = response.json().get("data")
# print(data)
pricing_options = data["results"][1].get("pricing_options")
legs = data["results"][1].get("legs")

print("Origin", legs[0].get("origin"))
print("Destination", legs[0].get("destination"))


climate_url = 'https://beta3.api.climatiq.io/travel/flights'
climate_headers = {
    'content-type': 'application/json',
    'Authorization' : 'Bearer CKA1H24HQ5M1JBGK2EXP8C3EV865'}
climate_data = {
        "legs": [
            {
                "from": "BER",
                "to": "HAM",
                "passengers": 2,
                "class": "first"
            },
            {
                "from": "HAM",
                "to": "JFK",
                "passengers": 2,
                "class": "economy"
            }
        ]
    }

response = requests.post(url=climate_url, headers=climate_headers, json=climate_data)
print(response.json().get("co2e"))

# for idx in range(len(pricing_options) - 2):
#     print(pricing_options[idx].get("price"))
#     # print("Duration of Flight", legs[idx].get("durationInMinutes"))

# print(f'Total users: {response.json().get("data")}')


# response = requests.get("https://api.open-notify.org/astros.json")
# print(response.status_code)

# requests.post('http://httpbin.org/post', json={"key": "value"})

# CKA1H24HQ5M1JBGK2EXP8C3EV865
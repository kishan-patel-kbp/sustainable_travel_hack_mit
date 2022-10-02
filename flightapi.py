import requests
import pandas as pd


# querystring = {"origin_iata": origin_iata,
# 	"period" : period, 
# 	"direct": direct,
# 	"one_way": one_way,
# 	"visa": visa,
# 	"locale": locale,
# 	"min_trip_duration_in_days": min_trip_duration_in_days,
# 	"max_trip_duration_in_days": max_trip_duration_in_days
# }

headers = {
	"X-Access-Token": "d752dc1bff39edfd08ce3ebef7e94f3d",
	"X-RapidAPI-Key": "2d3e34d72fmsha4c94eecaa8b6b5p1ea822jsnd0846372075f",
	"X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
}


def create_pd_df(period, origin_iata):
	# origin_iata = "BOS"
	# period = "2022-10-13"
	direct = "true"
	one_way = "false"
	visa = "false"
	locale = "en" #search language
	min_trip_duration_in_days = '4'
	max_trip_duration_in_days = '10'

	url = "http://map.aviasales.com/prices.json/?origin_iata="+origin_iata+"&period="+period+":season&direct="+direct+"&one_way="+one_way+"&schengen="+visa+"&locale="+locale+"&min_trip_duration_in_days="+min_trip_duration_in_days+"&max_trip_duration_in_days="+max_trip_duration_in_days

	response = requests.get(url, headers = headers)
	data = pd.DataFrame(response.json())[['value','ttl','trip_class','return_date','origin','number_of_changes','distance', 'destination', 'depart_date', 'airline']]
	return data

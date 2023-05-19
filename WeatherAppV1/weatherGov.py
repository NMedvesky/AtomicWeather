import datetime
import requests
import geocoder
import json


class Weather:
	def __init__(self):
		self.rawForecast = None
		self.forecast = list()

		self.city = None

		# Get Location
		self.lat, self.lng = geocoder.ip('me').latlng


	def getWeather(self):
		""" Send API Requests to weather.gov """

		# Send lat and lng to weather api to get hourly forecast url
		points_url = f"https://api.weather.gov/points/{self.lat},{self.lng}"
		response = requests.get(points_url).json()

		self.city = response["properties"]["relativeLocation"]["properties"]["city"]

		# Get forecast from weather api
		forecast_url = response["properties"]["forecastHourly"]
		self.rawForecast = requests.get(forecast_url).json()

		self.formatForecast()


	def formatForecast(self):
		""" Get Forecast For Each Hour """

		# Each period is a 1 hour range
		periods = self.rawForecast["properties"]["periods"]

		for period in periods:
			# Get Hour
			fullDate = datetime.datetime.fromisoformat(period["startTime"])
			dtHour = datetime.datetime.strptime(str(fullDate.hour), "%H")

			# Format Times
			hour = dtHour.strftime("%I %p")
			month = fullDate.strftime("%B")
			day = int(fullDate.day)

			# Determine the suffix for the day
			if 4 <= day <= 20 or 24 <= day <= 30:
			    suffix = "th"
			else:
			    suffix = ["st", "nd", "rd"][day % 10 - 1] if 1 <= day <= 3 else "th"

			formatedDate = f"{month} {day}{suffix} {hour}"

			date = {"fullDate": period["startTime"], "formatedDate": formatedDate, "hour": hour}

			# Grab Important Data From Json Response
			isDay = bool(period["isDaytime"])
			temp = int(period["temperature"])
			tempUnit = str(period["temperatureUnit"])
			windSpeed = int(period["windSpeed"][:-4])
			windDir = str(period["windDirection"])
			precipitationChance = int(period["probabilityOfPrecipitation"]["value"])
			relativeHumidity = int(period["relativeHumidity"]["value"])
			forecastDesc = str(period["shortForecast"])

			# Put Data Into One Dict
			hourForecast = {"city": self.city,
							"date": date,
							"isDay": isDay,
							"temp": temp,
							"tempUnit": tempUnit,
							"windSpeed": windSpeed,
							"windDir": windDir,
							"precipitationChance": precipitationChance,
							"relativeHumidity": relativeHumidity,
							"forecastDesc": forecastDesc}

			self.forecast.append(hourForecast)


if __name__ == "__main__":
	newForecast = Weather()

	newForecast.getWeather()
	newForecast.formatForecast()

	# Debuging json dump
	with open("weatherDump2.json", "w", encoding='utf-8') as jsonf:
		jsonf.write(json.dumps(newForecast.forecast, indent=4))

#!/usr/bin/python3
import requests, sys, time

class WeatherProvider:
	def __init__(self):
		self.cache = {}

	def getTemperature(self, city_name):
		if city_name in self.cache:
			if time.time() - self.cache[city_name]["time"] < (60 * 15):
				return self.cache[city_name]["temperature"]

		resp = requests.get(
			f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=b26111d32d394b084fe4ebfbdf849d26")

		if resp.status_code == 200:
			if not city_name in self.cache:
				self.cache[city_name] = {}
			self.cache[city_name]["temperature"] = resp.json()["main"]["temp"] - 273.15 # Kelvin
			self.cache[city_name]["time"] = time.time()
			return self.cache[city_name]["temperature"]

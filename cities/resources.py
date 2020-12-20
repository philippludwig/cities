#!/usr/bin/python3
import json, falcon, time
from .weather import WeatherProvider

cities = [
	{
		'name' : 'Leipzig',
		'id' : 1,
	},
	{
		'name' : 'Berlin',
		'id' : 2,
	},
	{
		'name' : 'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch',
		'id' : 3,
	},
	{
		'name' : 'Lüchtringen',
		'id' : 4,
	},
	{
		'name' : 'Stendal',
		'id' : 5,
	},
	{
		'name' : 'Eston',
		'id' : 6,
	},
	{
		'name' : 'Klaksvik',
		'id' : 7,
	},
	{
		'name' : 'Пермь',
		'id' : 8,
	},
	{
		'name' : 'الخرج',
		'id' : 9,
	},
	{
		'name' : 'თბილისი',
		'id' : 10,
	},
]

class CitiesResource(object):
	def __init__(self, weather_provider):
		self.weather_provider = weather_provider

	def on_get(self, req, resp):
		# Update temperature for all cities and set href
		for c in cities:
			c["temperature"] = self.weather_provider.getTemperature(c["name"])
			c["href"] = "/cities/" + str(c["id"])
		resp.body = json.dumps(cities, ensure_ascii=False)
		resp.status = falcon.HTTP_200

class CityResource(object):
	def __init__(self, weather_provider):
		self.weather_provider = weather_provider

	def get_city(self, id_or_name):
		it = filter(lambda c: str(c["id"]) == id_or_name or c["name"] == id_or_name, cities)
		try:
			city = next(it)
			city["temperature"] = self.weather_provider.getTemperature(city["name"])
			city["href"] = "/cities/" + city["name"]
			return city
		except StopIteration:
			return None

	def on_get(self, req, resp, id_or_name):
		city = self.get_city(id_or_name)
		if city == None:
			resp.status = falcon.HTTP_404
		else:
			resp.body = json.dumps(city, ensure_ascii=False)
			resp.status = falcon.HTTP_200

	def on_put(self, req, resp, id_or_name):
		if any(c["id"] == id_or_name or c["name"] == id_or_name for c in cities):
			resp.status = falcon.HTTP_200
			return

		cities.append({
			'name' : id_or_name,
			'id' : int(time.time()),
			'href' : '/cities/' + id_or_name,
		})
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(self.get_city(id_or_name), ensure_ascii=False)

	def on_delete(self, req, resp, id_or_name):
		if not any(c["id"] == id_or_name or c["name"] == id_or_name for c in cities):
			resp.status = falcon.HTTP_404

		else:
			cities[:] = [c for c in cities if c["id"] == id_or_name or c["name"] == id_or_name]
			resp.status == falcon.HTTP_200


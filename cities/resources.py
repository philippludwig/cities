#!/usr/bin/python3
import json, falcon, time
from .weather import WeatherProvider

cities = [
	{
		'name' : 'Leipzig',
		'id' : 1,
		'href' : '/cities/Leipzig'
	},
	{
		'name' : 'Berlin',
		'id' : 2,
		'href' : '/cities/Berlin'
	},
	{
		'name' : 'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch',
		'id' : 3,
		'href' : '/cities/Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch'
	}
]

class CitiesResource(object):
	def on_get(self, req, resp):
		resp.body = json.dumps(cities, ensure_ascii=False)
		resp.status = falcon.HTTP_200

class CityResource(object):
	def __init__(self):
		self.weather_provider = WeatherProvider()

	def on_get(self, req, resp, id_or_name):
		it = filter(lambda c: str(c["id"]) == id_or_name or c["name"] == id_or_name, cities)
		try:
			city = next(it)
			city["temperature"] = self.weather_provider.getTemperature(city["name"])
			resp.body = json.dumps(city, ensure_ascii=False)
			resp.status = falcon.HTTP_200
		except StopIteration:
			resp.status = falcon.HTTP_404

	def on_put(self, req, resp, id_or_name):
		if any(c["id"] == id_or_name or c["name"] == id_or_name for c in cities):
			resp.status = falcon.HTTP_200
			return

		cities.append({
			'name' : id_or_name,
			'id' : int(time.time()),
			'href' : '/cities/' + id_or_name
		})
		resp.status = falcon.HTTP_200

	def on_delete(self, req, resp, id_or_name):
		if not any(c["id"] == id_or_name or c["name"] == id_or_name for c in cities):
			resp.status = falcon.HTTP_404

		else:
			cities[:] = [c for c in cities if c["id"] == id_or_name or c["name"] == id_or_name]
			resp.status == falcon.HTTP_200


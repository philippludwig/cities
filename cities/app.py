#!/usr/bin/python3
import falcon
from falcon_cors import CORS
from .resources import CitiesResource, CityResource
from .weather import WeatherProvider

cors = CORS(allow_all_origins=True, allow_methods_list=["GET", "PUT"], allow_all_headers=True)
api = application = falcon.API(middleware=[cors.middleware])

weather_provider = WeatherProvider()
api.add_route('/cities', CitiesResource(weather_provider))
api.add_route('/cities/{id_or_name}', CityResource(weather_provider))

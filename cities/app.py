#!/usr/bin/python3
import appdirs, json, sys
import falcon
from falcon_cors import CORS
from .resources import CitiesResource, CityResource
from .weather import WeatherProvider

# Try to load config, which should contain the API key for the OpenWeatherMap
try:
	config_path = appdirs.user_config_dir() + "/cities.json"
	f = open(config_path, "r")
	config = json.load(f)
except:
	print("ERROR: Could not read config file:", config_path, file=sys.stderr)
	print("ERROR: Please create a config file `cities.json` which contains the API key.", file=sys.stderr)
	sys.exit(1)

try:
	weather_api_key = config["api_key"]
except:
	print("ERROR: Could not read the API key from the config.", config, file=sys.stderr)
	print("ERROR: Please add the attribute `api_key` to the config object.", file=sys.stderr)
	sys.exit(2)

weather_provider = WeatherProvider(weather_api_key)
cors = CORS(allow_all_origins=True, allow_methods_list=["GET", "PUT"], allow_all_headers=True)
api = application = falcon.API(middleware=[cors.middleware])

api.add_route('/cities', CitiesResource(weather_provider))
api.add_route('/cities/{id_or_name}', CityResource(weather_provider))

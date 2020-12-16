#!/usr/bin/python3
import falcon
from .resources import CitiesResource, CityResource
from falcon_cors import CORS

cors = CORS(allow_all_origins=True)
api = application = falcon.API(middleware=[cors.middleware])

api.add_route('/cities', CitiesResource())
api.add_route('/cities/{id_or_name}', CityResource())

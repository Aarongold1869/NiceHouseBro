# from django.conf import settings

from account.models import Account, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import Coordinates, MapData, Property

from functools import cache
from geopy.geocoders import Nominatim
# import http.client, urllib.parse
# import json
# import re
from typing import List

def filter_unsaved(account: Account, property_id: int)-> bool:
    saved_qs = SavedProperty.objects.filter(account=account)
    saved_ids = set([x.property_id for x in saved_qs])
    if (property_id in saved_ids):
        return False
    else:
        return True
    
def get_unsaved_properties(account: Account)-> List[Property]:
    property_list: List[Property] = PROPERTY_DATA
    filtered_list = list(filter(lambda x: filter_unsaved(account, x['id']), property_list))
    return filtered_list

# def position_stack_api(search_str: str)-> str:
#     conn = http.client.HTTPConnection('api.positionstack.com')
#     params = urllib.parse.urlencode({
#         'access_key': settings.POSITION_STACK_API_KEY,
#         'query': search_str,
#         # 'region': 'Rio de Janeiro',
#         'limit': 1,
#         })
#     conn.request('GET', '/v1/forward?{}'.format(params))
#     res = conn.getresponse()
#     data = res.read()
#     return json.loads(data)["data"][0]

@cache
def nominatim_boundry_api(search_str: str)-> str:
    app = Nominatim(user_agent="NHB")
    location = app.geocode(search_str, geometry='geojson')
    return location

LOCATION_TYPE_ZOOM_HASH = {
    'venue':  17,
    'address': 18,
    'street': 16,
    'neighbourhood': 14,
    'borough': 12,
    'localadmin': 12,
    'city': 11,
    'county': 8,
    'macrocounty': 16,
    'region': 5,
    'macroregion': 5,
    'country': 3,
    'coarse': 3,
    'postalcode': 10,
}

def retrieve_map_data_from_search_str(search_str: str)-> MapData:
    geocode_data = nominatim_boundry_api(search_str)
    addresstype = geocode_data.raw['addresstype']
    map_data: MapData = MapData( 
        coordinates=[geocode_data.latitude, geocode_data.longitude],
        boundry=geocode_data.raw['geojson'], 
        zoom=LOCATION_TYPE_ZOOM_HASH.get(addresstype, 11)
    )
    return map_data

def filter_properties_by_search(map_data: MapData)-> List[Property]:
    property_list: List[Property] = PROPERTY_DATA
    # filtered_list = list(filter(lambda x: x['coordinates'] == map_data['coordinates'], property_list))
    return property_list
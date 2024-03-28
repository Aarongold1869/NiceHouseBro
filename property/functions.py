# from django.conf import settings

from account.models import Account, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import Coordinates, MapData, Property

from functools import cache
from geopy.geocoders import Nominatim
import shapely.geometry as sg
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
    'building': 18,
    'street': 16,
    'neighbourhood': 14,
    'village': 13,
    'borough': 12,
    'localadmin': 12,
    'city': 11,
    'county': 9,
    'macrocounty': 16,
    'region': 5,
    'macroregion': 5,
    'country': 3,
    'coarse': 3,
    'postalcode': 10,
}

def retrieve_map_data_from_search_str(search_str: str)-> MapData | None:
    geocode_data = nominatim_boundry_api(search_str)
    if not geocode_data:
        return None
    addresstype = geocode_data.raw['addresstype']
    print(addresstype)
    map_data: MapData = MapData( 
        coordinates=[geocode_data.latitude, geocode_data.longitude],
        boundry=geocode_data.raw['geojson'], 
        zoom=LOCATION_TYPE_ZOOM_HASH.get(addresstype, 11),
        bounding_box=geocode_data.raw['boundingbox']
    )
    return map_data

def filter_properties_by_search_boundry(boundry: List[List[str]])-> List[Property]:
    def coordinates_are_in_polygon(coordinates, boundry):
        point = sg.Point(coordinates)
        polygon = sg.Polygon(boundry)
        return point.within(polygon)
    inverted_boundry = [(elem2, elem1) for elem1, elem2 in boundry]
    filtered_list = list(filter(lambda x: coordinates_are_in_polygon(x['Coordinates'], inverted_boundry), PROPERTY_DATA))
    return filtered_list

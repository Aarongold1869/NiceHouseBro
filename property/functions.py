from django.conf import settings

from account.models import Account, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import Coordinates, MapData, Property

from functools import cache
from geopy.geocoders import GoogleV3, Nominatim
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

@cache
def nominatim_boundry_api(search_str: str, reverse: bool)-> dict | None:
    app = Nominatim(user_agent="NHB")
    if not reverse:
        location = app.geocode(search_str, geometry='geojson')
    else:
        # app = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        res = app.reverse(search_str)
        if not res:
            return None
        location = app.geocode(res.raw['address'], geometry='geojson')
    return location

LOCATION_TYPE_ZOOM_HASH = {
    'venue':  17,
    'address': 18,
    'building': 18,
    'street': 16,
    'neighbourhood': 14,
    'suburb': 13,
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
    geocode_data = nominatim_boundry_api(search_str=search_str, reverse=False)
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

def retrieve_map_data_from_reverse_search(search_str: str)-> MapData | None:
    geocode_data = nominatim_boundry_api(search_str=search_str, reverse=True)
    if not geocode_data:
        return None
    addresstype = geocode_data.raw['addresstype']
    map_data: MapData = MapData( 
        coordinates=[geocode_data.latitude, geocode_data.longitude],
        boundry=geocode_data.raw['geojson'], 
        zoom=LOCATION_TYPE_ZOOM_HASH.get(addresstype, 11),
        bounding_box=geocode_data.raw['boundingbox']
    )
    return map_data

def filter_properties_by_search_boundry(boundry: List[Coordinates])-> List[Property]:
    def coordinates_are_in_polygon(coordinates: Coordinates, boundry: List[Coordinates])-> bool:
        point = sg.Point([coordinates[1], coordinates[0]])
        if type(boundry[0][0]) == float:
            polygon = sg.Polygon(boundry)
        else:
            polygon = sg.Polygon(boundry[0])
        return point.within(polygon)
    filtered_list: List[Property] = list(filter(lambda x: coordinates_are_in_polygon(x['Coordinates'], boundry), PROPERTY_DATA))
    return filtered_list

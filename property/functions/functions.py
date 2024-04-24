from profiles.models import Profile, SavedProperty
# from .api.test_api import PROPERTY_DATA
from ..api.google_api import google_street_view_api
from ..api.nominatim_api import nominatim_boundry_api
from ..types import Coordinates, MapData, Property

import shapely.geometry as sg
from typing import List, TypedDict

# def filter_unsaved(profile: Profile, property_id: int)-> bool:
#     saved_qs = SavedProperty.objects.filter(profile=profile)
#     saved_ids = set([x.property_id for x in saved_qs])
#     if (property_id in saved_ids):
#         return False
#     else:
#         return True
    
# def get_unsaved_properties(profile: Profile)-> List[Property]:
#     property_list: List[Property] = PROPERTY_DATA
#     filtered_list = list(filter(lambda x: filter_unsaved(profile, x['id']), property_list))
#     return filtered_list

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
    'state': 7,
    'macroregion': 5,
    'country': 3,
    'coarse': 3,
    'postalcode': 10,
}

def retrieve_map_data_from_search_str(search_str: str)-> MapData:
    geocode_data = nominatim_boundry_api(search_str=search_str)
    if not geocode_data:
        return None
    addresstype = geocode_data.raw['addresstype']
    coordinates = geocode_data.raw['geojson']['coordinates'][0]
    if type(coordinates[0][0]) == float:
        boundry = coordinates
    else:
        boundry = coordinates[0]
    map_data: MapData = MapData( 
        coordinates=[geocode_data.latitude, geocode_data.longitude],
        boundry=boundry, 
        zoom=LOCATION_TYPE_ZOOM_HASH.get(addresstype, 11),
        bounding_box=geocode_data.raw['boundingbox'],
        address=geocode_data.raw['address']
    )
    return map_data

def retrieve_map_data_from_reverse_search(search_str: str)-> MapData:
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

class ImageDict(TypedDict):
    propertyId: str
    image: str

def get_card_image_arr(property_list: List[Property], get_all:bool=False)-> List[str]:
    image_arr = []
    for i in range(len(property_list)):
        if (i <= 1 or i == len(property_list) - 1) or get_all:
            property_obj = property_list[i]
            saved_qs = SavedProperty.objects.filter(property_id=property_obj['propertyId'])
            address = f"{property_obj['streetLine']} {property_obj['city']}, {property_obj['state']} {property_obj['postalCode']}"
            if saved_qs.exists():
                image = saved_qs[0].image if saved_qs[0].image else google_street_view_api(address=address)
            else:
                image = google_street_view_api(address=address)
            image_arr.append(image)
        else:
            image_arr.append(None)
    return image_arr

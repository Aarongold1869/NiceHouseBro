from django.conf import settings

from profiles.models import Profile, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import Address, Coordinates, MapData, Property

from functools import cache, reduce
from geopy.geocoders import GoogleV3, Nominatim
import shapely.geometry as sg
from typing import List

import urllib.request, urllib.parse, urllib.error
import requests

def filter_unsaved(profile: Profile, property_id: int)-> bool:
    saved_qs = SavedProperty.objects.filter(profile=profile)
    saved_ids = set([x.property_id for x in saved_qs])
    if (property_id in saved_ids):
        return False
    else:
        return True
    
def get_unsaved_properties(profile: Profile)-> List[Property]:
    property_list: List[Property] = PROPERTY_DATA
    filtered_list = list(filter(lambda x: filter_unsaved(profile, x['id']), property_list))
    return filtered_list

@cache
def nominatim_boundry_api(search_str: str, reverse: bool)-> dict | None:
    app = Nominatim(user_agent="NHB")
    if not reverse:
        location = app.geocode(search_str, geometry='geojson', addressdetails=True)
    else:
        # app = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        res = app.reverse(search_str)
        if not res:
            return None
        location = app.geocode(res.raw['address'], geometry='geojson', addressdetails=True)
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
        bounding_box=geocode_data.raw['boundingbox'],
        address=geocode_data.raw['address']
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

def remove_slashes_from_address(address: str)-> str:
    return address.replace('/', '|')

def property_search_api(address: Address)-> List[Property]:
    url = 'https://api.realestateapi.com/v2/PropertySearch'
    headers = {
        "accept": "application/json",
        "x-api-key": settings.NOTION_API_KEY,
        "content-type": "application/json"
    }
    payload = {
        "ids_only": False,
        "obfuscate": False,
        "summary": False,
        # "size": 3,
        # "Latitude": coordinates[0],
        # "Longitude": coordinates[1],
        # "radius": 50,
        "city": address['city'],
        "state": address['ISO3166-2-lvl4'][3:],
        # "negative_equity": True,
        # "equity": True,
        # "cash_buyer": True,
        # "quit_claim": True,
        # "corporate_owned": True,
        # "free_clear": True,
        # "absentee_owner": True,
        # "reo": True,
        # "auction": True,
        # "foreclosure": True,
        # "pre_foreclosure": True,
        # "beds_min": 2,
        # "beds_max": 4
    }
    property_list = []
    try: 
        res = requests.post(url, headers=headers, json=payload)
        if not res.ok:
            print('Error: ', res['message'])
            return property_list
        property_list = res.json()['data']
        res.close()
        property_list = list(filter(lambda x: 'address' in x.keys() and 'address' in x['address'].keys(), property_list))
    except requests.exceptions.RequestException as e:
        print(e)
    return property_list

def property_detail_api(address: str)-> Property:
    url = "https://api.realestateapi.com/v2/PropertySearch"
    payload = {
        "ids_only": False,
        "obfuscate": False,
        "summary": False,
        "size": 1,
        "address": address
    }
    headers = {
        "accept": "application/json",
        "x-api-key": settings.NOTION_API_KEY,
        "content-type": "application/json"
    }
    property = None
    try: 
        res = requests.post(url, headers=headers, json=payload)
        if not res.ok:
            print('Error: ', res['message'])
            return property
        property = res.json()['data'][0]
        res.close()
    except requests.exceptions.RequestException as e:
        print(e)
    return property


def google_street_view_api(address:str):
    params = {
        "key": settings.GOOGLE_MAPS_API_KEY,
        "location": address,
        "size": "600x300"
    }
    res = requests.get('https://maps.googleapis.com/maps/api/streetview', params=params)
    if res.ok:
        f_path = f'static/media/property-images/{address}.jpg'
        with open(f_path, 'wb') as file:
            file.write(res.content)
        res.close()
    return f_path.split('static/')[1]
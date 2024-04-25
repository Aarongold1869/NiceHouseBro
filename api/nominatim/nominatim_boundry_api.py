from .types import MapData, NominatimApiReponse

from functools import lru_cache
from geopy.geocoders import Nominatim

@lru_cache
def nominatim_boundry_api(search_str: str, reverse:bool=False)-> NominatimApiReponse:
    app = Nominatim(user_agent="NHB")
    if not reverse:
        location: NominatimApiReponse = app.geocode(search_str, geometry='geojson', addressdetails=True)
    else:
        # app = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        res = app.reverse(search_str)
        if not res:
            return None
        location: NominatimApiReponse = app.geocode(res.raw['address'], geometry='geojson', addressdetails=True)
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
    'state': 7,
    'macroregion': 5,
    'country': 3,
    'coarse': 3,
    'postalcode': 10,
}

def fetch_map_data_from_search_str(search_str: str)-> MapData:
    geocode_data: NominatimApiReponse = nominatim_boundry_api(search_str=search_str)
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

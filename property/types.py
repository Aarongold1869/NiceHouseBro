from typing import TypedDict, List

class Coordinates(TypedDict):
    lat: float
    lng: float

class MapData(TypedDict):
    coordinates: Coordinates
    boundry: List[str]
    zoom: int
    bounding_box: List[str]

class Property(TypedDict):
    # Zillow zestimate API
    id: str
    city: str
    state: str
    address: str
    postal_code: str
    Laitude: float
    Longitude: float
    Coordinates: List[float]
    zestimate: int
    rental_zestimate: int
    # other property details 
    price: int 
    bedrooms: int 
    bathrooms: int 
    area: int 
    cap_rate: float 
    cover_image_url: str 
    image_array: List[str] 
    is_saved: bool | None


class NominatimApiReponse(TypedDict):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    class_: str
    type: str
    place_rank: int
    importance: float
    addresstype: str
    name: str
    display_name: str
    boundingbox: List[str]

    {'place_id': 292037873,
     'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
     'osm_type': 'relation',
     'osm_id': 1128379,
     'lat': '28.5421109',
     'lon': '-81.3790304',
     'class': 'boundary',
     'type': 'administrative',
     'place_rank': 16,
     'importance': 0.6305938364430198,
     'addresstype': 'city',
     'name': 'Orlando',
     'display_name': 'Orlando, Orange County, Florida, United States',
     'boundingbox': [
         '28.3480634',
        '28.6142830',
        '-81.5075377',
        '-81.2275862'
    ]
}
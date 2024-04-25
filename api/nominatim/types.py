from typing import TypedDict, List

class Coordinates(TypedDict):
    lat: float
    lng: float

class Address(TypedDict):
    address: str
    city: str
    county: str
    state: str
    street: str
    zip: int

class MapData(TypedDict):
    coordinates: Coordinates
    boundry: List[str]
    zoom: int
    bounding_box: List[str]
    address: Address

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
    geojson: List[str]
    addressdetails: Address
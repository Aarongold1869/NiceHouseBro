from typing import TypedDict

from .property_list import *

class Coordinates(TypedDict):
    lat: float
    long: float

class BoundryData(TypedDict): 
    city: str
    county: str
    state: str
    postal_code: str

from .scraper import RedfinScraper
from .redfin_types import Property
from ..nominatim.types import  MapData

import shapely.geometry as sg
from typing import List

def fetch_property_list_from_map_data(map_data: MapData)-> List[Property]:
    poly = sg.Polygon(map_data['boundry'])
    simple = poly.simplify(0.01, preserve_topology=False)
    poly_str = ''
    for x, y in simple.exterior.coords:
        poly_str += f'{x}%20{y}%2C'
    scraper = RedfinScraper(
        include_nearby_homes=True, 
        market=map_data['address']['city'], 
        num_homes=50,
        page_number=1, 
        poly=poly_str
    )
    property_list: List[Property] = scraper.get_property_list()
    return property_list


def property_detail_api():
    ...
    
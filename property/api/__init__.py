from .redfin.scraper import RedfinScraper
from .redfin.redfin_types import Property

from property.functions import retrieve_map_data_from_search_str

import shapely.geometry as sg
from typing import List

def property_search_api(search_str: str)-> List[Property]:
    map_data = retrieve_map_data_from_search_str(search_str=search_str)
    poly = sg.Polygon(map_data['boundry'])
    # simple = poly.simplify(0.01, preserve_topology=False)
    poly_str = ''
    for x, y in poly.exterior.coords:
        poly_str += f'{x}%20{y}%2C'
    scraper = RedfinScraper(
        include_nearby_homes=True, 
        market=map_data['address']['city'], 
        num_homes=350,
        page_number=1, 
        poly=poly_str
    )
    property_list: List[Property] = scraper.get_property_list()
    return property_list


def property_detail_api():
    ...
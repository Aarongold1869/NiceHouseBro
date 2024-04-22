from django.test import TestCase

# Create your tests here.
from .api.redfin.scraper import RedfinScraper
from .api.redfin.redfin_types import Property
from typing import List

import matplotlib.pyplot as plt
import shapely.geometry as sg
from shapely import normalize
from shapely.ops import cascaded_union

from .functions import retrieve_map_data_from_search_str

class MainTest(TestCase):
    def setUp(self):
       ...
        

    def test_main(self):
        search_str = 'Hermosa Beach, CA'
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
from django.test import TestCase

# Create your tests here.
from .api.redfin.scraper import RedfinScraper
from .api.redfin.redfin_types import Property
from typing import List

import matplotlib.pyplot as plt
import shapely.geometry as sg

from .functions import retrieve_map_data_from_search_str

class MainTest(TestCase):
    def setUp(self):
       ...
        

    def test_main(self):
        search_str = 'Newark, NJ'
        map_data = retrieve_map_data_from_search_str(search_str=search_str)
        poly = sg.Polygon(map_data['boundry'])
        simple = poly.simplify(0.01, preserve_topology=False)
        # plt.plot(*simple.exterior.xy)
        # plt.show()
        poly_str = ''
        for x, y in simple.exterior.coords:
            poly_str += f'{x}%20{y}%2C'
        print(poly_str)
        scraper = RedfinScraper(
            include_nearby_homes=True, 
            market=map_data['address']['city'], 
            num_homes=1,
            page_number=1, 
            poly=poly_str
        )
        print(scraper.get_endpoint())
        data: List[Property] = scraper.get_property_list()
        if len(data) > 0:
            print(data)
from .scraper import RedfinScraper, RedfinPropertyDetailScraper
from .redfin_types import Property
from ..nominatim.types import  MapData

import shapely.geometry as sg
from typing import List

from functools import lru_cache


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
    ### for testing only ###
    # property_list = json.load(open('api/redfin/test/property_list.json'))
    return property_list

@lru_cache
def property_detail_api(state:str, city:str, address:str, zip:int, propertyId:str)-> Property:
    print('scraping redfin')
    scraper = RedfinPropertyDetailScraper(state=state, city=city, address=address, zip=zip, id=propertyId)
    property = scraper.get_property_detail_data()
    print(property)
    # property = {
    #     'propertyId': 0, 
    #     'address': address, 
    #     'latLong': {
    #         'value':{
    #             'latitude':47.4998584,
    #             'longitude':-122.3360967
    #         }
    #     },
    #     'price': 230000, 
    #     'cap_rate': 0.1,
    #     'beds': '3', 
    #     'baths': '1', 
    #     'sq_ft': '1,607', 
    #     'remarks': 'Charming 3-bedroom, 1-bathroom home nestled in the heart of OKC. Recent updates include new sewer plumbing and hallway ceilings, and ceiling fans in 2023; new roof and interior paint in 2022, and backyard grass seed and leveling in 2024. Newer hot water tank and HVAC overhaul in 2019, along with a new electrical panel and windows in 2015. Featuring an open concept layout that blends modern updates with original character, this home includes a sunroom for added relaxation. The primary bedroom offers a spacious closet with washer and dryer hookups. Outside, the backyard includes a storage shed. Conveniently located within walking distance to Reed Park, local restaurants, grocery stores, and numerous shopping options, this property offers both comfort and convenience in a desirable neighborhood. ', 
    #     'photo': 'https://ssl.cdn-redfin.com/photo/254/bigphoto/591/644591_0.jpg'
    # }
    return property
    
    
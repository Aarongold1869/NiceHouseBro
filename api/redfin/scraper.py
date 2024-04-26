from bs4 import BeautifulSoup
from functools import lru_cache
import json
import requests
from typing import List, Dict
import urllib

import sys
if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
    from .redfin_types import Property, RedfinResponse
else:
    from redfin_types import Property, RedfinResponse

class RedfinScraper():
    def __init__(self, include_nearby_homes: bool, market:str, poly:str, num_homes:int=10, page_number:int=1):
        self.al = 1
        self.include_nearby_homes = str(include_nearby_homes).lower()
        # self.market = market
        self.num_homes = num_homes
        self.ord = 'redfin-recommended-asc'
        self.page_number = page_number
        self.poly = poly
        self.sf = '1,2,3,5,6,7'
        self.start = 0
        self.status = 1
        self.uipt = '1,2,3,4,5,6,7,8'

    def get_endpoint(self)-> str:
        endpoint = 'gis?' + urllib.parse.urlencode(self.__dict__, safe=',%')                                                                                                                         #-122.54472%2047.44109%2C-122.11144%2047.44109%2C-122.11144%2047.78363%2C-122.54472%2047.78363%2C-122.54472%2047.44109'
        return endpoint
    
    def get_property_list(self)-> List[Property]:
        base_url = 'https://www.redfin.com/stingray/api/'
        url = base_url + self.get_endpoint()
        headers={  
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pretty: RedfinResponse = soup.prettify().replace('{}&amp;&amp;', '')
            data = json.loads(pretty)["payload"]
            property_list = []
            if 'homes' in data:
                return data['homes']
            elif 'originalHomes' in data:
                return data['originalHomes']['homes']
            return property_list
        else:
            print(response.status_code)
            print('Failed to scrape the URL')
            return []


class RedfinPropertyDetailScraper():
    def __init__(self, state:str, city:str, address:str, id:int):
        self.state = state
        self.city = city
        self.address = address
        self.id = id

    def get_endpoint(self)-> str:
        endpoint = f'{self.state}/{self.city}/{self.address}/home/{self.id}'
        return endpoint
    
    def get_soup(self)-> Dict:
        # https://www.redfin.com/TN/Elizabethton/121-Williams-Ave-37643/home/116345480
        base_url = 'https://www.redfin.com/'
        url = base_url + self.get_endpoint()
        headers={  
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
        }
        response = requests.get(url, headers=headers)
        if not response.status_code == 200:
            print(response.status_code)
            print('Failed to scrape the URL')
            return None
        soup: RedfinResponse = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_property_detail_data(self)-> Dict:
        soup = self.get_soup()
        if not soup:
            return None
        home_stats = soup.find_all('div', class_='home-main-stats-variant')
        stat_blocks = home_stats[0].find_all('div', class_='stat-block')
        stats = {}
        print(stat_blocks)
        for el in stat_blocks:
            key = el.find(class_='statsLabel').text
            val = el.find(class_='statsValue').text
            stats[key] = val 
        return stats


def test_search_scraper():
    scraper = RedfinScraper(
        include_nearby_homes=True, 
        market='seattle', 
        num_homes=1,
        page_number=1, 
        poly='-122.54472%2047.44109%2C-122.11144%2047.44109%2C-122.11144%2047.78363%2C-122.54472%2047.78363%2C-122.54472%2047.44109'
    )
    data: List[Property] = scraper.get_property_list()
    if len(data) > 0:
        print(data)


def test_detail_scraper():
    scraper = RedfinPropertyDetailScraper(
        state='OK',
        city='Oklahoma City',
        address='3028-NW-13th-St-73107',
        id=78551049
    )
    data = scraper.get_property_detail_data()
    if data:
        print(data)

def main():
    # test_search_scraper()
    test_detail_scraper()

if __name__ == '__main__':
    main()



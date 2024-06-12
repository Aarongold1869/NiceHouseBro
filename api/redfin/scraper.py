from django.conf import settings

from bs4 import BeautifulSoup
from functools import lru_cache
import json
import re
import requests
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from typing import List, Dict
import urllib
from .redfin_types import Property, RedfinResponse
# from redfin_types import Property, RedfinResponse

# SCRAPFLY
SCRAPFLY_API_KEY = settings.SCRAPFLY_API_KEY
SCRAPFLY = ScrapflyClient(key=SCRAPFLY_API_KEY)

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
    
    @lru_cache
    def get_property_list(self)-> List[Property]:
        print('fetch property list')
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
    def __init__(self, state:str, city:str, address:str, zip:int, id:int):
        self.state = state
        self.city = city
        self.address = address
        self.zip = zip
        self.id = id

    def get_endpoint(self)-> str:
        if '#' in self.address:
            street_line, apt_number = self.address.split('#')
            return f'{self.state}/{self.city}/{street_line.replace(" ","-")}-{self.zip}/unit-{apt_number}/home/{self.id}'
        return f'{self.state}/{self.city}/{self.address.replace(" ","-")}-{self.zip}/home/{self.id}'
    
    def get_response(self, scrap_fly=False)-> Dict | ScrapeApiResponse | None:
        # https://www.redfin.com/TN/Elizabethton/121-Williams-Ave-37643/home/116345480
        base_url = 'https://www.redfin.com/'
        url = base_url + self.get_endpoint()
        if not scrap_fly:
            headers={  
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
            }
            response = requests.get(url, headers=headers)
        else:
            response = SCRAPFLY.scrape(ScrapeConfig(url=url, asp=True, country="US", render_js=True))
        if not response.status_code == 200:
            print(response.status_code)
            print('Failed to scrape the URL')
            return None
        # soup: RedfinResponse = BeautifulSoup(response.text, 'html.parser')
        # soup: RedfinResponse = response.soup
        return response

    def parse_response(self)-> Dict:
        response = self.get_response()
        if not response:
            response = self.get_response(scrap_fly=True)
            soup = response.soup
        else: 
            soup: RedfinResponse = BeautifulSoup(response.text, 'html.parser')
            
        if not soup:
            return None
        
        data = {}
        top_stats = soup.find_all('div', class_='home-main-stats-variant')
        stat_blocks = top_stats[0].find_all('div', class_='stat-block')
        for el in stat_blocks:
            key = el.find(class_='statsLabel').text.replace(' ', '_').lower()
            if 'get_pre-approved' in key:
                key = 'price'
            val = el.find(class_='statsValue').text
            data[key] = val 
        data['remarks'] = soup.find('div', class_='remarks').find('p').find('span').text
        data['images'] = []
        images = soup.findAll('span', id=re.compile('^MBImage'))
        for image in images:
            data['images'].append(image.find('img')['src'])
        return data


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



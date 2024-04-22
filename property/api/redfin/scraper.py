from bs4 import BeautifulSoup
import json
import requests
from typing import List
import urllib

from .redfin_types import Property, RedfinResponse

class RedfinScraper():

    def __init__(self, include_nearby_homes: bool, market:str, num_homes:int, page_number:int, poly:str):
        self.al = 1
        self.include_nearby_homes = str(include_nearby_homes).lower()
        self.market = market
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
            print(data['originalHomes'].keys())
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
    
def main():
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

if __name__ == '__main__':
    main()



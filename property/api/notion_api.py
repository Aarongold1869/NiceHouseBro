from django.conf import settings

from property.types import Address, Property

from functools import lru_cache
import requests
from typing import List, TypedDict

class NotionApiPayload(TypedDict):
    ids_only: bool
    obfuscate: bool
    summary: bool
    size: int
    Latitude: float
    Longitude: float
    radius: int
    address: str
    city: str
    state: str
    negative_equity: bool
    equity: bool
    cash_buyer: bool
    quit_claim: bool
    corporate_owned: bool
    free_clear: bool
    absentee_owner: bool
    reo: bool
    auction: bool
    foreclosure: bool
    pre_foreclosure: bool
    beds_min: int
    beds_max: int


def property_search_api(address: Address, size:int=250, min:int=20000, max:int=0)-> List[Property]:
    url = 'https://api.realestateapi.com/v2/PropertySearch'
    headers = {
        "accept": "application/json",
        "x-api-key": settings.NOTION_API_KEY,
        "content-type": "application/json"
    }
    payload: NotionApiPayload = {
        "ids_only": False,
        "size": size,
        "obfuscate": False,
        "summary": False,
        "state": address['ISO3166-2-lvl4'][3:]
    }
    if 'city' in address.keys():
        payload['city'] = address['city']
    if max > 0:
        payload['value_max'] = max
    if min > 0:
        payload['value_min'] = min

    property_list: List[Property] = []
    try: 
        res = requests.post(url, headers=headers, json=payload)
        if not res.ok:
            print('Error: ', res['message'])
            return property_list
        property_list = res.json()['data']
        res.close()
        required = ['address', 'suggestedRent']
        property_list = list(filter(lambda x: set(required).issubset(x.keys()) and 'address' in x['address'].keys(), property_list)) # require address and suggestedRent
    except requests.exceptions.RequestException as e:
        print(e)
    return property_list

@lru_cache
def property_detail_api(address: str)-> Property:
    url = "https://api.realestateapi.com/v2/PropertySearch"
    payload: NotionApiPayload = {
        "ids_only": False,
        "obfuscate": False,
        "summary": False,
        
        "size": 1,
        "address": address
    }
    headers = {
        "accept": "application/json",
        "x-api-key": settings.NOTION_API_KEY,
        "content-type": "application/json"
    }
    
    property = None
    try: 
        res = requests.post(url, headers=headers, json=payload)
        if not res.ok:
            print('Error: ', res['message'])
            return property
        property = res.json()['data'][0]
        res.close()
    except requests.exceptions.RequestException as e:
        print(e)
    return property
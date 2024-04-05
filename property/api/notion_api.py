from django.conf import settings

from property.types import Address, Property

from functools import cache
import requests
from typing import List, NotRequired, TypedDict

class NotionApiPayload(TypedDict):
    ids_only: bool
    obfuscate: bool
    summary: bool
    size: NotRequired[int]
    Latitude: NotRequired[float]
    Longitude: NotRequired[float]
    radius: NotRequired[int]
    address: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    negative_equity: NotRequired[bool]
    equity: NotRequired[bool]
    cash_buyer: NotRequired[bool]
    quit_claim: NotRequired[bool]
    corporate_owned: NotRequired[bool]
    free_clear: NotRequired[bool]
    absentee_owner: NotRequired[bool]
    reo: NotRequired[bool]
    auction: NotRequired[bool]
    foreclosure: NotRequired[bool]
    pre_foreclosure: NotRequired[bool]
    beds_min: NotRequired[int]
    beds_max: NotRequired[int]

def property_search_api(address: Address, size:int=50, min:int=0, max:int=0)-> List[Property]:
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
        property_list = list(filter(lambda x: 'address' in x.keys() and 'address' in x['address'].keys(), property_list))
    except requests.exceptions.RequestException as e:
        print(e)
    return property_list

@cache
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
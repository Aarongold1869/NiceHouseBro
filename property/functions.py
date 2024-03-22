from account.models import Account, SavedProperty
from property.data import PROPERTY_DATA, Property

import re
from typing import List

def filter_unsaved(account: Account, property_id: int)-> bool:
    saved_qs = SavedProperty.objects.filter(account=account)
    saved_ids = set([x.property_id for x in saved_qs])
    if (property_id in saved_ids):
        return False
    else:
        return True
    
def get_unsaved_properties(account: Account)-> List[Property]:
    property_list: List[Property] = PROPERTY_DATA
    filtered_list = list(filter(lambda x: filter_unsaved(account, x['id']), property_list))
    return filtered_list

def filter_property_list(get, property_list)-> List[Property]:
    ...

def process_search_str(search_str: str)-> str:
    zip_regex = r'^\d{5}(?:[-\s]\d{4})?$'
    zip = re.search(zip_regex, search_str)
    print('zip', zip)
    return zip
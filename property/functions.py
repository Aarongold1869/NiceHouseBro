from account.models import Account, SavedProperty
from property.data import PROPERTY_DATA, Property

from typing import List

def filter_unsaved(account: Account, property_id: int):
    saved_qs = SavedProperty.objects.filter(account=account)
    saved_ids = set([x.property_id for x in saved_qs])
    if (property_id in saved_ids):
        return False
    else:
        return True
    
def get_unliked_properties(account: Account):
    property_list: List[Property] = PROPERTY_DATA
    filtered_list = list(filter(lambda x: filter_unsaved(account, x['id']), property_list))
    return filtered_list
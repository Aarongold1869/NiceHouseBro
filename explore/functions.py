from api.google import google_street_view_api
from api.redfin.redfin_types import Property
from profiles.models import SavedProperty

from typing import List, TypedDict

class ImageDict(TypedDict):
    propertyId: str
    image: str

def fetch_card_image_arr(property_list: List[Property], get_all:bool=False)-> List[str]:
    image_arr = []
    for i in range(len(property_list)):
        if (i <= 1 or i == len(property_list) - 1) or get_all:
            property_obj = property_list[i]
            saved_qs = SavedProperty.objects.filter(property_id=property_obj['propertyId'])
            # address = f"{property_obj['streetLine']} {property_obj['city']}, {property_obj['state']} {property_obj['postalCode']}"
            if saved_qs.exists():
                image = saved_qs[0].image if saved_qs[0].image else google_street_view_api(address=property_obj['address'])
            else:
                image = google_street_view_api(address=property_obj['address'])
            image_arr.append(image)
        else:
            image_arr.append(None)
    return image_arr

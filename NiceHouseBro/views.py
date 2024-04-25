from django.conf import settings
from django.shortcuts import render

from api.redfin import fetch_property_list_from_map_data
from api.redfin.redfin_types import Property
from explore.functions import fetch_card_image_arr

from typing import List

def home_view(request):
    # property_list: List[Property] = property_search_api(search_str='Pensacola, FL')
    property_list: List[Property] = []
    # image_arr = get_card_image_arr(property_list=property_list, get_all=True)
    card_img_arr = []
    context = {
        'property_list': property_list, 
        'card_img_arr': card_img_arr,
    }
    return render(request, 'home.html', context)
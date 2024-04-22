from django.conf import settings
from django.shortcuts import render

from property.api import property_search_api
from property.functions import get_card_image_arr
from property.types import Property

from typing import List

def home_view(request):
    property_list: List[Property] = property_search_api(search_str='Pensacola, FL')
    image_arr = get_card_image_arr(property_list=property_list, get_all=True)
    context = {
        'property_list': property_list, 
        'image_arr': image_arr,
        'API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'home.html', context)
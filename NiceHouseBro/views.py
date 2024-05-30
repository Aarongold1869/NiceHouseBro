from django.conf import settings
from django.shortcuts import render

from api.redfin import fetch_property_list_from_map_data
from api.redfin.redfin_types import Property

from typing import List

def home_view(request):
    # property_list: List[Property] = property_search_api(search_str='Pensacola, FL')
    property_list: List[Property] = []
    context = {
        'property_list': property_list, 
    }
    return render(request, 'home.html', context)
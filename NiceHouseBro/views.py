from django.conf import settings
from django.shortcuts import render

from property.api.test_api import PROPERTY_DATA
from property.types import Property

from typing import List

def home_view(request):
    property_list: List[Property] = PROPERTY_DATA
    return render(request, 'home.html', {'property_list': property_list, 'API_KEY': settings.GOOGLE_MAPS_API_KEY, })
from django.shortcuts import render

from property.data import PROPERTY_DATA, Property

from typing import List

def home_view(request):
    property_list: List[Property] = PROPERTY_DATA
    return render(request, 'home.html', {'property_list': property_list })

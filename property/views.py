from django.shortcuts import render

from property.data import PROPERTY_DATA, Property

from typing import List

def home_view(request):
    property_list: List[Property] = PROPERTY_DATA
    return render(request, 'home.html', {'property_list': property_list })

def property_detail_view(request, property_id: int):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    return render(request, 'property/property-detail.html', {'property': property })
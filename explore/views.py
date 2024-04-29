from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from api.redfin import fetch_property_list_from_map_data
from api.redfin.redfin_types import Property
from api.google import google_street_view_api
from api.nominatim import fetch_map_data_from_search_str #, retrieve_map_data_from_reverse_search
from api.nominatim.types import MapData

from profiles.models import Profile
from property.models import SavedProperty
from .functions import fetch_card_image_arr
from property.functions import calculate_cap_rate

import random
from typing import List

def explore_view(request, search_str:str='Pensacola, FL'):
    ''' View recieves search string as an argument and returns a list of properties, 
    and map data based on the search string. If no search string is provided, the 
    view returns data for Pensacola, FL.'''

    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    
    # fetch property list from map data (specifically boundry info)
    property_list: List[Property] = fetch_property_list_from_map_data(map_data=map_data)
    # calculate cap rate for each property
    # create address string for each property
    property_list = list(map(lambda x: { 
                                **x, 
                                'cap_rate': calculate_cap_rate(value=int(x['price']['value']), rent=random.randint(1000, 2000)),
                                'address': f"{x['streetLine']['value'] if 'value' in x['streetLine'] else x['streetLine']} {x['city']}, {x['state']} {x['postalCode']['value']}"
                            }, property_list))
    property_init = None
    is_saved = False
    card_img_arr = None
    if len(property_list) > 0:
        property_init = property_list[0]
        is_saved = SavedProperty.objects.filter(property_id=property_init['propertyId']).exists()
        card_img_arr = fetch_card_image_arr(property_list)

    context = {
        'map_data': map_data,
        'property_list': property_list, 
        'property_obj': property_init,
        'card_img_arr': card_img_arr,
        'is_saved': is_saved,
        'search_str': search_str
    }
    return render(request, "explore/explore.html", context)

@require_http_methods(['GET'])
def get_explore_controls_view(request, property_id: str):
    address = request.GET.get('address')
    is_saved = False
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property_id) & Q(archived=False))
        is_saved = saved_qs.exists()
    return render(request, 'explore/partials/explore-controls.html', { 'property_obj': { 'propertyId': property_id, "address": { "address": address } }, 'is_saved': is_saved })

@require_http_methods(['GET'])
def get_card_image_view(request, *args, **kwargs):
    property_id = request.GET.get('property_id')
    address = request.GET.get('address')
    image = google_street_view_api(address=address)
    return render(request, 'explore/partials/card-image.html', {'property_id': property_id, 'image': image})

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved_explore_view(request, property_id: str):
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            profile=profile,
            property_id=property_id,
            address=request.POST.get('address'),
            image=request.POST.get('image')
        )
        is_saved = True
        # toast = { "type": "success", "header": "Explore", "message": "Property saved!" }
    else:
        saved_qs.delete()
        is_saved = False
        # toast = { "type": "success", "header": "Explore", "message": "Property unsaved." }
    context = {
        'property_id': property_id,
        'is_saved': is_saved,
        # 'toast': toast,
    }
    return render(request, 'explore/partials/explore-save-button.html', context)


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

from django_htmx.http import trigger_client_event
import json
import random
from typing import List


def explore_view(request, search_str:str='Pensacola, FL'):
    ''' View recieves search string as an argument and returns a list of properties, 
    and map data based on the search string. If no search string is provided, the 
    view returns data for Pensacola, FL.'''

    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    
    if not request.htmx:
        # fetch property list from map data (specifically boundry info)
        property_list: List[Property] = fetch_property_list_from_map_data(map_data=map_data)
        # calculate cap rate for each property
        # create address string for each property
        property_list = list(map(lambda x: { 
                                **x, 
                                'cap_rate': calculate_cap_rate(value=int(x['price']['value']), rent=random.randint(1000, 2000)),
                                'address': f"{x['streetLine']['value'] if 'value' in x['streetLine'] else x['streetLine']} {x['city']}, {x['state']} {x['postalCode']['value']}",
                                'is_saved': SavedProperty.objects.filter(property_id=x['propertyId']).exists(),
                                'image': None
                            }, property_list))

    else:
        property_list = json.loads(json.dumps(request.POST.getlist('property_list')))
        property_list = list(map(lambda x: json.loads(x), property_list))
        filters = json.loads(request.POST.get('filter_form'))
        property_list = list(filter(lambda x: x["cap_rate"] >= float(filters['cap-rate']), property_list))  

    property_init = None
    if len(property_list) > 0:
        property_init = property_list[0]
        end = 2 if len(property_list) > 2 else len(property_list)
        for i in range(-1, end):
            property_list[i]['image'] = google_street_view_api(address=property_list[i]['address'])

    context = {
        'map_data': map_data,
        'property_list': property_list, 
        'property_obj': property_init,
        'search_str': search_str
    }
    return render(request, "explore/explore.html", context)

@require_http_methods(['POST'])
def filter_properties(request, *args, **kwargs):
    property_list = request.POST.getlist('property_list')
    filters = request.POST.get('filter_form')
    property_list = list(filter(lambda x: x['cap_rate'] >= filters['cap-rate'], property_list))
    return HttpResponse(status=200)

@require_http_methods(['GET'])
def get_card_image_view(request, *args, **kwargs):
    property_id = request.GET.get('property_id')
    address = request.GET.get('address')
    image = google_street_view_api(address=address)
    return render(request, 'explore/partials/card-image.html', {'property_id': property_id, 'image': image})

import ast 
@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved_explore_view(request):
    profile = Profile.objects.get(user=request.user)
    property_obj = Property(**json.loads(json.dumps(request.POST)))
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_obj['propertyId']))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            profile=profile, 
            property_id=property_obj['propertyId'],
            address=property_obj['address'],
            image=property_obj['image'],
            price=property_obj['price'],
            cap_rate=property_obj['cap_rate'],
            beds=property_obj['beds'],
            baths=property_obj['baths'],
            sq_ft=property_obj['sq_ft']
        )
        property_obj['is_saved'] = True
    else:
        saved_qs.delete()
        property_obj['is_saved'] = False
    return render(request, 'explore/partials/explore-save-button.html', { 'property': property_obj  })


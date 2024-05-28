from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from api.redfin import fetch_property_list_from_map_data
from api.redfin.redfin_types import Property
from api.google import google_street_view_api_base64
from api.nominatim import fetch_map_data_from_search_str 
from api.nominatim.types import MapData

from profiles.models import Profile
from property.models import SavedProperty
from property.functions import calculate_cap_rate

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
    # fetch property list from map data (specifically boundry info)
    property_list: List[Property] = fetch_property_list_from_map_data(map_data=map_data)
    # calculate cap rate for each property
    # create address string for each property
    property_list = list(map(lambda x: { 
                            **x, 
                            'cap_rate': calculate_cap_rate(value=int(x['price']['value']), rent=random.randint(1000, 2000)),
                            'address': f"{x['streetLine']['value'] if 'value' in x['streetLine'] else x['streetLine']} {x['city']}, {x['state']} {x['postalCode']['value']}",
                            'is_saved': SavedProperty.objects.filter(property_id=x['propertyId']).exists(),
                            # 'image': None
                        }, property_list))
    property_init = None
    if len(property_list) > 0:
        property_init = property_list[0]
        end = 2 if len(property_list) > 2 else len(property_list)
        for i in range(-1, end):
            property_list[i]['image'] = google_street_view_api_base64(address=property_list[i]['address'])

    context = {
        'map_data': map_data,
        'property_list': property_list, 
        'property_obj': property_init,
        'search_str': search_str,
        'filters': {
            'cap_rate': 0,
            'min_price': 0,
            'max_price': '',
            'beds': '',
            'baths': '',
            'sq_ft': ''
        }
    }
    return render(request, "explore/explore.html", context)

def explore_view_filtered(
        request, 
        search_str:str='Pensacola, FL', 
        cap_rate:str=0, 
        min_price:int=0,
        max_price:int=0,
        beds:int=0,
        baths:int=0,
        sq_ft:int=0,
        *args, 
        **kwargs
    ):
    ''' View recieves search string as an argument and returns a list of properties, 
    and map data based on the search string. If no search string is provided, the 
    view returns data for Pensacola, FL.'''

    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    
    property_list: List[Property] = fetch_property_list_from_map_data(map_data=map_data)
    property_list = list(
        map(lambda x: { 
                **x, 
                'cap_rate': calculate_cap_rate(value=int(x['price']['value']), rent=random.randint(1000, 2000)),
                'address': f"{x['streetLine']['value'] if 'value' in x['streetLine'] else x['streetLine']} {x['city']}, {x['state']} {x['postalCode']['value']}",
                'is_saved': SavedProperty.objects.filter(property_id=x['propertyId']).exists(),
                # 'image': None
            }, filter(lambda x: x["cap_rate"] >= float(cap_rate), property_list)
        )
    )
    property_init = None
    if len(property_list) > 0:
        property_init = property_list[0]
        end = 2 if len(property_list) > 2 else len(property_list)
        for i in range(-1, end):
            property_list[i]['image'] = google_street_view_api_base64(address=property_list[i]['address'])

    context = {
        'map_data': map_data,
        'property_list': property_list, 
        'property_obj': property_init,
        'search_str': search_str,
        'filters': {
            'cap_rate': cap_rate,
            'min_price': min_price,
            'max_price': max_price,
            'beds': beds,
            'baths': baths,
            'sq_ft': sq_ft
        }
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
    image = google_street_view_api_base64(address=address)
    return render(request, 'explore/partials/card-image.html', {'property_id': property_id, 'image': image})


import base64
from django.core.files.base import ContentFile

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved_explore_view(request):
    profile = Profile.objects.get(user=request.user)
    property_data = json.loads(json.dumps(request.POST))
    property_id = property_data.get('propertyId', None)
    address = property_data.get('address', None)
    if not property_id or not address:
        return HttpResponse(status=400)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        price = property_data.get('price', 0)
        beds = property_data.get('beds', 0)
        baths = property_data.get('baths', 0)
        sq_ft = property_data.get('sq_ft', 0)
        saved_property = SavedProperty.objects.create(
            profile = profile, 
            property_id = property_id,
            address = address,
            price = price if not type(price) == str else 0,
            cap_rate = property_data.get('cap_rate', 0),
            beds = beds if not type(beds) == str else 0,
            baths = baths if not type(baths) == str else 0,
            sq_ft = sq_ft if not type(sq_ft) == str else 0
        )

        image_data = property_data.get('image', None)
        if not image_data:
            image_data = google_street_view_api_base64(address=address)
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))  
        file_name = f"{property_id}.{ext}"
        try:
            saved_property.image.save(file_name, data, save=True)
        except:
            pass
        property_data['is_saved'] = True
    else:
        saved_qs.delete()
        property_data['is_saved'] = False
    return render(request, 'explore/partials/explore-save-button.html', { 'property': property_data  })


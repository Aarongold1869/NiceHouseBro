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

import random
from typing import List


def get_additional_property_list_context(property_data: List[Property], user_profile:Profile):

    def set_property_obj_context(obj, user_profile):
        price = obj['price']['value'] if 'value' in obj['price'] else 0
        obj['price'] = price
        obj['cap_rate'] = calculate_cap_rate(value=int(price), rent=random.randint(1000, 2000))
        obj['address'] = obj['streetLine']['value'] if 'value' in obj['streetLine'] else obj['streetLine']
        obj['address_full'] = f"{obj['streetLine']['value'] if 'value' in obj['streetLine'] else obj['streetLine']} {obj['city']}, {obj['state']} {obj['postalCode']['value']}"
        obj['is_saved'] = SavedProperty.objects.filter(property_id=obj['propertyId']).filter(profile=user_profile).exists()
        obj['street'] = obj['streetLine']['value'] if 'value' in obj['streetLine'] else obj['streetLine']
        obj['sq_ft'] = obj['sqFt']['value'] if 'value' in obj['sqFt'] else '-'
        return obj
    
    property_list = list(map(lambda x: { **x, **set_property_obj_context(x, user_profile) }, property_data))
    if len(property_list) > 0:
        end = 2 if len(property_list) > 2 else len(property_list)
        for i in range(-1, end):
            property_list[i]['image'] = google_street_view_api_base64(address=property_list[i]['address'])
    return property_list


def explore_view(request, search_str:str='Pensacola, FL'):
    ''' View recieves search string as an argument and returns a list of properties, 
    and map data based on the search string. If no search string is provided, the 
    view returns data for Pensacola, FL.'''

    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    redfin_property_data: List[Property] = fetch_property_list_from_map_data(map_data=map_data)
    property_list = get_additional_property_list_context(property_data=redfin_property_data, user_profile=Profile.objects.filter(user=request.user.id).first())
    context = {
        'map_data': map_data,
        'property_list': property_list, 
        'property_obj': property_list[0] if len(property_list) > 0 else None,
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


def filter_property_list(property_list: List[Property], filters: dict):
    filtered_property_list = list(filter(lambda x: x["cap_rate"] >= float(filters['cap_rate']), property_list))
    return filtered_property_list

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

    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    redfin_property_data: List[Property] = fetch_property_list_from_map_data(map_data=map_data)
    property_list = get_additional_property_list_context(property_data=redfin_property_data, user_profile=Profile.objects.filter(user=request.user.id).first())
    filters = { 
        'cap_rate':cap_rate, 
        'min_price':min_price,
        'max_price':max_price,
        'beds':beds,
        'baths':baths,
        'sq_ft':sq_ft,
    }
    filtered_property_list = filter_property_list(property_list=property_list, filters=filters)
    context = {
        'map_data': map_data,
        'property_list': filtered_property_list, 
        'property_obj': filtered_property_list[0] if len(filtered_property_list) > 0 else None,
        'search_str': search_str,
        'filters': filters
    }
    return render(request, "explore/explore.html", context)

@require_http_methods(['GET'])
def get_card_image_view(request, *args, **kwargs):
    property_id = request.GET.get('property_id')
    address = request.GET.get('address')
    image = google_street_view_api_base64(address=address)
    if len(image) == 0:
        image = '/media/property_images/default/awesome-house.jpg'
    return render(request, 'explore/partials/card-image.html', {'property_id': property_id, 'image': image})



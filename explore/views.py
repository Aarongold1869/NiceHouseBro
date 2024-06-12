from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from api.redfin import fetch_property_list_from_map_data
from api.redfin.redfin_types import Property
from api.google import google_street_view_api_base64
from api.nominatim import fetch_map_data_from_search_str 
from api.nominatim.types import MapData

from account.models import CustomUser
from profiles.models import Profile, UserSearches, CapRateFormula
from profiles.forms import CapRateForm
from property.models import SavedProperty
from property.functions import calculate_cap_rate

import after_response
import random
from typing import List

def get_search_str(user: CustomUser):
    search_qs = UserSearches.objects.filter(profile__user=user)
    if search_qs.exists():
        return search_qs.last().search_str 
    elif user.profile.location:
        return user.profile.location
    return 'Pensacola, FL'

@after_response.enable
def set_last_search(user, search_str:str):
    if user.is_authenticated:
        UserSearches.objects.create(profile=user.profile, search_str=search_str)

def get_additional_property_list_context(property_data: List[Property], user_profile: Profile, cap_rate_formula: CapRateFormula):

    def set_property_obj_context(obj, user_profile):
        price = obj['price']['value'] if 'value' in obj['price'] else 0
        random.seed(obj['propertyId'])
        print(obj['propertyId'], type(obj['propertyId']))
        rent = random.randint(900, 2500)
        *_, cap_rate = calculate_cap_rate(
            value=int(price), 
            rent=rent, 
            annual_property_tax_rate=cap_rate_formula.annual_property_tax_rate,
            monthly_management_fee_rate=cap_rate_formula.monthly_management_fee_rate,
            monthly_maintance_as_rate=cap_rate_formula.monthly_maintance_as_rate,
            monthly_insurance=cap_rate_formula.monthly_insurance,
            monthly_leasing_fee=cap_rate_formula.monthly_leasing_fee,
            monthly_hoa_fee=cap_rate_formula.monthly_hoa_fee,
            monthly_utilities=cap_rate_formula.monthly_utilities,
        )
        obj['price'] = price
        obj['rent'] = rent
        obj['cap_rate'] = float(cap_rate)
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


def explore_view(request, search_str:str=None, *args, **kwargs):
    ''' View recieves search string as an argument and returns a list of properties, 
    and map data based on the search string. If no search string is provided, the 
    view returns data for Pensacola, FL.'''
    if not search_str:
        if request.user.is_authenticated:
            search_str = get_search_str(request.user)
        else:
            search_str = 'Pensacola, FL'
    
    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    set_last_search.after_response(request.user, search_str)
    redfin_property_data: List[Property] = fetch_property_list_from_map_data(map_data=map_data)

    cap_rate_formula = CapRateFormula()
    if request.user.is_authenticated:
        cap_rate_formula, created = CapRateFormula.objects.get_or_create(profile=request.user.profile)
        
    property_list = get_additional_property_list_context(property_data=redfin_property_data, user_profile=request.user.profile, cap_rate_formula=cap_rate_formula)
    
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
        },
        'cap_rate_form': CapRateForm(instance=cap_rate_formula)
    }
    return render(request, "explore/explore.html", context)


def filter_property_list(property_list: List[Property], filters: dict):
    filtered_property_list = list(filter(lambda x: x["cap_rate"] >= float(filters['cap_rate']), property_list))
    return filtered_property_list

def explore_view_filtered(
        request, 
        search_str:str=None,
        cap_rate:str=0, 
        min_price:int=0,
        max_price:int=0,
        beds:int=0,
        baths:int=0,
        sq_ft:int=0,
        *args, 
        **kwargs
    ):

    if not search_str:
        if request.user.is_authenticated:
            search_str = get_search_str(request.user)
        else:
            search_str = 'Pensacola, FL'

    map_data: MapData = fetch_map_data_from_search_str(search_str=search_str) 
    if not map_data:
        return HttpResponse(status=500)
    set_last_search.after_response(request.user, search_str)
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
    return render(request, 'explore/partials/card-image.html', {'property_id': property_id, 'image': image})



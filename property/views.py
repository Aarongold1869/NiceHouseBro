from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from profiles.models import Profile, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import Address, Property
from .functions import (
    retrieve_map_data_from_search_str, 
    retrieve_map_data_from_reverse_search, 
    filter_properties_by_search_boundry, 
    google_street_view_api,
    property_detail_api,
    property_search_api,
)

from typing import List

def explore_view(request, search_str=None, lat=None, lng=None):
    map_data = None
    property_list: List[Property] = []
    
    if search_str and search_str != '':
        map_data = retrieve_map_data_from_search_str(search_str=search_str)
        if not map_data:
            raise Exception("Map data not found.")
        # currently only notion api is used
        property_list = property_search_api(address=map_data['address'])
        # property_list = list(map(lambda x: {**x , 'image': google_street_view_api(address=x['address']['address'])}, property_list[:10]))

    if lat and lng:
        map_data = retrieve_map_data_from_reverse_search(search_str=f"{lng}, {lat}")
        if not map_data:
            response = render(request, '500.html', {})
            response.delete_cookie('coordinates')
            return response
        # currently only notion api is used
        property_list = property_search_api(address=map_data['address'])

    template = "property/explore.html"

    context = {
        'property_list': property_list, 
        'property_id': property_list[0]['propertyId'] if property_list else -1, 
        'is_saved': False,
        'property_init': property_list[0] if property_list else None,
        'API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'map_data': map_data,
        'search_str': search_str if search_str else ''
    }
    return render(request, template, context)

@require_http_methods(['GET'])
def get_explore_controls_view(request, property_id: str):
    saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property_id))
    is_saved = False if not saved_qs.exists() else True
    return render(request, 'property\partials\explore-controls.html', {'property_id': property_id, 'is_saved': is_saved })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved_explore_view(request, property_id: str):
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            profile=profile,
            property_id=property_id
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
    return render(request, 'property/partials/explore-save-button.html', context)

def property_detail_view(request, address:str='5663 Dunridge Drive, Pace FL 32571'):
    property: Property = property_detail_api(address=address)
    street_view_image = google_street_view_api(address=address)
    is_saved = False
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property['propertyId']))
        if saved_qs.exists():
            is_saved = True
    return render(request, 'property/property-detail.html', {'property': property, "is_saved": is_saved, "image": street_view_image })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved(request, property_id: str):
    # property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(profile=profile, property_id=property_id)
        # property['saved'] = True
        is_saved = True
    else:
        saved_qs.delete()
        # property['saved'] = False
        is_saved = False
    return render(request, "property/partials/detail-save-button.html", {'property_id': property_id, 'is_saved': is_saved  })
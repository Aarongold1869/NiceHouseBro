from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from profiles.models import Profile, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import Property
from .functions import retrieve_map_data_from_search_str, retrieve_map_data_from_reverse_search, filter_properties_by_search_boundry

from typing import List

@require_http_methods(['GET'])
def explore_view(request, search_str=None, lat=None, lng=None):
    map_data = None
    property_list: List[Property] = []
    
    if search_str and search_str != '':
        map_data = retrieve_map_data_from_search_str(search_str=search_str)
        if not map_data:
            raise Exception("Map data not found.")
        property_list = filter_properties_by_search_boundry(boundry=map_data['boundry']['coordinates'][0])

    if lat and lng:
        map_data = retrieve_map_data_from_reverse_search(search_str=f"{lng}, {lat}")
        # print(map_data)
        if not map_data:
            response = render(request, '500.html', {})
            response.delete_cookie('coordinates')
            return response
        property_list = filter_properties_by_search_boundry(boundry=map_data['boundry']['coordinates'][0])

    template = "property/explore.html"
    property_id = property_list[0]['id'] if property_list else -1

    context = {
        'property_list': property_list, 
        'property_id': property_id, 
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

@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def toggle_property_saved_explore_view(request, property_id: str):
    # property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
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

def property_detail_view(request, property_id: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property_id))
        if saved_qs.exists():
            property['saved'] = True
    return render(request, 'property/property-detail.html', {'property': property })

@require_http_methods(['GET'])
def toggle_property_descripton(request, property_id: str, action: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    if action == 'show':
        template = "property/partials/expanded-desc.html"
    elif action == 'hide':
        template = "property/partials/truncated-desc.html"
    return render(request, template, {'property': property })

@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def toggle_property_saved(request, property_id: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(profile=profile, property_id=property_id)
        property['saved'] = True
        template = "property/partials/button-saved.html"
    else:
        saved_qs.delete()
        property['saved'] = False
        template = "property/partials/button-unsaved.html"
    return render(request, template, {'property': property })
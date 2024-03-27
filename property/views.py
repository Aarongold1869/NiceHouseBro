from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from account.models import Account, SavedProperty
from .api.property_list import PROPERTY_DATA
from .types import MapData, Property
from .functions import retrieve_map_data_from_search_str, filter_properties_by_search

from typing import List

def home_view(request):
    property_list: List[Property] = PROPERTY_DATA
    return render(request, 'property/home.html', {'property_list': property_list, 'API_KEY': settings.GOOGLE_MAPS_API_KEY, })

@login_required(login_url='/accounts/login/')
@require_http_methods(['GET'])
def explore_view(request, search_str=None):
    # account = Account.objects.get(user=request.user)
    map_data: MapData = {'zoom': 13}
    if search_str:
        map_data = retrieve_map_data_from_search_str(search_str)
    property_list: List[Property] = filter_properties_by_search(map_data)
    template = "property/explore.html"
    property_id = property_list[0]['id'] if property_list else -1
    # if request.htmx:
    #     property_list = filter_property_list(request.GET, property_list)
    #     template = "property/partials/property-card-container.html"
    context = {
        'property_list': property_list, 
        'property_id': property_id, 
        'is_saved': False,
        'property_init': property_list[0] if property_list else None,
        'API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'map_data': map_data
    }
    return render(request, template, context)

@require_http_methods(['GET'])
def get_explore_controls_view(request, property_id: str):
    saved_qs = SavedProperty.objects.filter(Q(account__user=request.user) & Q(property_id=property_id))
    is_saved = False if not saved_qs.exists() else True
    return render(request, 'property\partials\explore-controls.html', {'property_id': property_id, 'is_saved': is_saved })

@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def toggle_property_saved_explore_view(request, property_id: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    account = Account.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(account=account) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            account=account,
            property_id=property_id
        )
        is_saved = True
        toast = { "type": "success", "header": "Explore", "message": "Property saved!" }
    else:
        saved_qs.delete()
        is_saved = False
        toast = { "type": "success", "header": "Explore", "message": "Property unsaved." }
    return render(request, 'property/partials/explore-save-button.html', {'property_id': property_id, 'toast': toast, 'is_saved':is_saved })

def property_detail_view(request, property_id: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(account__user=request.user) & Q(property_id=property_id))
        if saved_qs.exists():
            property['saved'] = True
    return render(request, 'property/property-detail.html', {'property': property })

def toggle_property_descripton(request, property_id: str, action: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    if action == 'show':
        template = "property/partials/expanded-desc.html"
    elif action == 'hide':
        template = "property/partials/truncated-desc.html"
    return render(request, template, {'property': property })

def toggle_property_saved(request, property_id: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    account = Account.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(account=account) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(account=account, property_id=property_id)
        property['saved'] = True
        template = "property/partials/button-saved.html"
    else:
        saved_qs.delete()
        property['saved'] = False
        template = "property/partials/button-unsaved.html"
    return render(request, template, {'property': property })
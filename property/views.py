from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from account.models import Account, SavedProperty
from .data import PROPERTY_DATA, Property
from .functions import get_unliked_properties

from typing import List

def home_view(request):
    property_list: List[Property] = PROPERTY_DATA
    return render(request, 'property/home.html', {'property_list': property_list })

@login_required(login_url='/accounts/login/')
def explore_view(request):
    account = Account.objects.get(user=request.user)
    property_list: List[Property] = get_unliked_properties(account)
    template = "property/explore.html"
    property_id = property_list[0]['id'] if property_list else -1
    return render(request, template, {'property_list': property_list, 'property_id': property_id })

@require_http_methods(['GET'])
def get_explore_controls_view(request, property_id: str):
    return render(request, 'property\partials\explore-controls.html', {'property_id': property_id })

@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def save_property_explore_view(request, property_id: str):
    # property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    account = Account.objects.get(user=request.user)
    SavedProperty.objects.get_or_create(
        account=account,
        property_id=property_id
    )
    return HttpResponse(status=201)

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
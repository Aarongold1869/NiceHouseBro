from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
@require_http_methods(['GET', 'POST'])
def explore_view(request):
    account = Account.objects.get(user=request.user)
    property_list: List[Property] = get_unliked_properties(account)
    index = 0
    template = "property/explore.html"
    if request.htmx: 
        index = int(request.POST.get('index', 0))
        action = request.POST.get('action', None)
        template = "property/partials/property-card.html"
        if action == 'save':
            property_id = request.POST.get('property_id')
            SavedProperty.objects.create(account=account, property_id=property_id)
            property_list: List[Property] = get_unliked_properties(account)
        else:
            index += 1
        if index >= len(property_list):
            if len(property_list) == 0:
                template = "property/partials/end-of-list.html"
            else:
                index = 0
    property = property_list[index] if index < len(property_list) else None
    return render(request, template, {'property': property, 'index': index})

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
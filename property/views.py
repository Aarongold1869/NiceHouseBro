from django.db.models import Q
from django.shortcuts import render

from account.models import Account, SavedProperty
from property.data import PROPERTY_DATA, Property

from typing import List

def home_view(request):
    property_list: List[Property] = PROPERTY_DATA
    return render(request, 'home.html', {'property_list': property_list })

def property_detail_view(request, property_id: int):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(account__user=request.user) & Q(property_id=property_id))
        if saved_qs.exists():
            property['saved'] = True
    return render(request, 'property/property-detail.html', {'property': property })

def toggle_property_descripton(request, property_id: int, action: str):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    if action == 'show':
        template = "property/partials/expanded-desc.html"
    elif action == 'hide':
        template = "property/partials/truncated-desc.html"
    return render(request, template, {'property': property })

def toggle_property_saved(request, property_id: int):
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
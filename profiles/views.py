from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Profile, SavedProperty
from property.api.property_list import PROPERTY_DATA
from property.types import Property

import json

# Create your views here.
@login_required(login_url='/account/login/')

def saved_property_list_view(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    saved_properties = SavedProperty.objects.filter(profile=profile)
    saved_properties_list = [x.property_id for x in saved_properties]
    saved_properties_data = [x for x in PROPERTY_DATA if x['id'] in saved_properties_list]
    return render(request, 'profile/saved-properties.html', {'saved_properties': saved_properties_data })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_saved(request, property_id: str, *args, **kwargs):
    property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(profile=profile, property_id=property_id)
    if saved_qs.exists():
        saved_qs.delete()
        template = 'profile/partials/property-removed.html'
    else:
        SavedProperty.objects.create(profile=profile, property_id=property_id)
        template = 'profile/partials/saved-property-card.html'
    return render(request, template, {"property": property})


def locate_view(request, *args, **kwargs):
    response = HttpResponse(status=200)
    response.set_cookie('coordinates', json.dumps(request.GET))
    return response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Profile, SavedProperty
from property.api.notion_api import property_detail_api
from property.types import Property

import ast
import json

# Create your views here.
@login_required(login_url='/account/login/')

def saved_property_list_view(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    saved_properties_qs = SavedProperty.objects.filter(profile=profile).filter(archived=False).order_by('-timestamp')
    property_list = list(map(lambda x: {
                                **property_detail_api(address=x.address), 
                                'image': x.image
                            }, saved_properties_qs ))
    return render(request, 'profile/saved-properties.html', {'saved_properties': property_list })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_saved_property_archived(request, property_id: str, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(profile=profile, property_id=property_id)
    property_obj = ast.literal_eval(request.POST.get('property_obj', None))
    if not saved_qs.exists():
        return HttpResponse(status=500)
    saved_property = saved_qs.first()
    saved_property.archived = not saved_property.archived
    saved_property.save()
    if saved_property.archived:
        template = 'profile/partials/property-removed.html'
    else:
        template = 'profile/partials/saved-property-card.html'
    return render(request, template, {"property": property_obj })

@login_required(login_url='/account/login/')
@require_http_methods(['GET'])
def toggle_theme(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    if profile.theme == 'light':
        profile.theme = 'dark'
    else:
        profile.theme = 'light'
    profile.save()
    return HttpResponse(status=200)

def locate_view(request, *args, **kwargs):
    response = HttpResponse(status=200)
    response.set_cookie('coordinates', json.dumps(request.GET))
    return response
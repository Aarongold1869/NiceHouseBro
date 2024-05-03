from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from django_htmx.http import trigger_client_event

from .models import Profile, BlockedUser, GOAL_CHOICES
from .forms import UpdateProfileForm
from property.models import SavedProperty
from api.redfin import property_detail_api

import ast
import json
import os

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
def update_profile_view(request, *args, **kwargs):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.htmx:
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('first_name')
            user = form.cleaned_data.get('last_name')
            user = form.cleaned_data.get('email')
            user.save()
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.location = form.cleaned_data.get('location')
            profile.goal = form.cleaned_data.get('goal')
            profile.save()
            return HttpResponse(status=200)
    return render(request, 'profile/update-profile.html', {'profile': profile, 'GOAL_CHOICES': GOAL_CHOICES })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def update_profile_picture(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    file = request.FILES.get('file-input', None)
    if file:
        if profile.profile_picture:
            if os.path.exists(profile.profile_picture.path):
                os.remove(profile.profile_picture.path)
        profile.profile_picture = file
        profile.save()
    return render(request, 'profile/partials/profile-img.html', {'profile': profile })

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

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def block_user_view(request, blocked_user_id:int ):
    if request.user.id == blocked_user_id:
        return HttpResponse(status=500)
    profile = Profile.objects.get(user=request.user)
    BlockedUser.objects.create(profile=profile, blocked_user=blocked_user_id)
    response = HttpResponse(status=200)
    return trigger_client_event(response, 'reload-comments')
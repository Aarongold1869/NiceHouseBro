from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from profiles.models import Profile, SavedProperty
from api.google import google_street_view_api
from api.redfin import property_detail_api
from api.redfin.redfin_types import Property

def property_detail_view(request, address:str='5663 Dunridge Drive, Pace FL 32571'):
    property = property_detail_api(address=address)
    # street_view_image = google_street_view_api(address=address)
    is_saved = False
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property['propertyId']))
        is_saved = saved_qs.exists()
    return render(request, 'property/property-detail.html', {'property': property, "is_saved": is_saved })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved(request, property_id: str):
    # property: Property = next((x for x in PROPERTY_DATA if x['id'] == property_id), None)
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            profile=profile, 
            property_id=property_id,
            address=request.POST.get('address'),
            image=request.POST.get('image')
        )
        # property['saved'] = True
        is_saved = True
    else:
        saved_qs.delete()
        # property['saved'] = False
        is_saved = False
    return render(request, "property/partials/detail-save-button.html", {'property_id': property_id, 'is_saved': is_saved  })
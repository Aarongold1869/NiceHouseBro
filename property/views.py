from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import SavedProperty
from comment.forms import CommentForm, ReportFormForm
from comment.models import Comment, CommentLike, ReplyLike
from profiles.models import Profile, BlockedUser
from agent.forms import AgentContactFormForm
from agent.models import AgentContactForm
from api.google import google_street_view_api_base64
from api.redfin import property_detail_api
from api.redfin.redfin_types import Property

from .functions import calculate_cap_rate

import after_response
import base64
import json
import random

def property_detail_view(request, state:str, city:str, address:str, zip:int, propertyId:str):
    property = property_detail_api(state='FL', city=city, address=address, zip=zip, propertyId=propertyId)
    property['cap_rate'] = calculate_cap_rate(int(property['price'].replace('$','').replace(',','')), random.randint(1000, 2000))
    # street_view_image = google_street_view_api_base64(address=address)
    is_saved = False
    contact_form = AgentContactFormForm()
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=propertyId))
        is_saved = saved_qs.exists()
        contact_form = None
        contact_form_qs = AgentContactForm.objects.filter(Q(user=request.user) & Q(address=address))
        if not contact_form_qs.exists():
            contact_form = AgentContactFormForm(initial = {
                'user': request.user,
                'name': request.user.get_full_name(),
                'email': request.user.email,
                'phone': Profile.objects.get(user=request.user).phone_number,
                'address': address,
            })
    property = { **property, 'propertyId': propertyId, 'address': address, 'state': state, 'city': city, 'zip': zip, 'is_saved': is_saved }
    context = { 'property': property, 'contact_form': contact_form }
    return render(request, 'property/property-detail.html', context)

@require_http_methods(['GET'])
def retrieve_comment_section(request, property_id: str):
    comment_list = Comment.objects.filter(property_id=property_id).order_by('-timestamp')
    context = {
        'property': {'propertyId': property_id},
        'form': CommentForm(),
        'comment_list': comment_list,
        'report_form': ReportFormForm()
    }
    if request.user.is_authenticated:
        context['comment_like_list'] = list(map(lambda x: x.comment.id, CommentLike.objects.filter(profile__user=request.user, comment__property_id=property_id)))
        context['reply_like_list'] = list(map(lambda x: x.reply.id, ReplyLike.objects.filter(profile__user=request.user)))
        context['blocked_user_list'] = list(map(lambda x: x.blocked_user, BlockedUser.objects.filter(profile__user=request.user)) )
    return render(request, 'comment/comment-section.html', context)

@after_response.enable
def process_model_image(saved_property: SavedProperty, image_data):
    if not image_data or not 'base64' in image_data:
        image_data = google_street_view_api_base64(address=saved_property.address_full)
    format, imgstr = image_data.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr))  
    file_name = f"{saved_property.property_id}.{ext}"
    try:
        saved_property.image.save(file_name, data, save=True)
    except:
        pass
    return

@login_required()
@require_http_methods(['POST'])
def toggle_property_saved(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    property_data = None
    try:
        property_data: Property = json.loads(request.POST.get('property'))
        print(property_data['price'])
    except:
        return HttpResponse(status=400)
    property_id = property_data.get('propertyId', None)
    address = property_data.get('address', None)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        price = property_data.get('price', 0)
        if type(price) == str:
            price = int(price.replace('$', '').replace(',', ''))
        beds = property_data.get('beds', 0)
        baths = property_data.get('baths', 0)
        sq_ft = property_data.get('sq_ft', 0)
        saved_property = SavedProperty.objects.create(
            profile = profile, 
            property_id = property_id,
            address = address,
            city = property_data.get('city', ''),
            state = property_data.get('state', ''),
            zip = property_data.get('zip', 0),
            price = price if not type(price) == str else 0,
            cap_rate = property_data.get('cap_rate', 0),
            beds = beds if not type(beds) == str else 0,
            baths = baths if not type(baths) == str else 0,
            sq_ft = sq_ft if not type(sq_ft) == str else 0
        )
        saved_property.save()
        process_model_image.after_response(saved_property, property_data.get('photo', None))
        property_data['is_saved'] = True
    else:
        saved_qs.delete()
        property_data['is_saved'] = False

    view = request.POST.get('view', None)
    if view == 'detail':
        template = 'property/partials/detail-save-button.html'
    elif view == 'explore':
        template = 'explore/partials/explore-save-button.html'  
    elif view == 'profile':
        template = 'profile/partials/property-removed.html'
    return render(request, template, { 'property': property_data  })


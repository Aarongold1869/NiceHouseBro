from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import SavedProperty
from comment.forms import CommentForm, ReportFormForm
from comment.models import Comment, CommentLike, ReplyLike
from profiles.models import Profile, BlockedUser
from agent.forms import AgentContactFormForm
from agent.models import AgentContactForm
from api.google import google_street_view_api
from api.redfin import property_detail_api
from api.redfin.redfin_types import Property

import json


def property_detail_view(request, address:str='5663 Dunridge Drive, Pace FL 32571'):
    property = property_detail_api(address=address)
    # street_view_image = google_street_view_api(address=address)
    is_saved = False
    contact_form = AgentContactFormForm()
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property['propertyId']))
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
    return render(request, 'property/property-detail.html', { 'property': property, 'is_saved': is_saved, 'contact_form': contact_form })

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

import ast 
@login_required()
@require_http_methods(['POST'])
def toggle_property_saved_detail(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    property_obj = Property(**json.loads(json.dumps(request.POST)))
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_obj['propertyId']))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            profile=profile, 
            property_id=property_obj['propertyId'],
            address=property_obj['address'],
            image=property_obj['image'],
            price=property_obj['price'],
            cap_rate=property_obj['cap_rate'],
            beds=property_obj['beds'],
            baths=property_obj['baths'],
            sq_ft=property_obj['sq_ft']
        )
        property_obj['is_saved'] = True
    else:
        saved_qs.delete()
        property_obj['is_saved'] = False
    return render(request, "property/partials/detail-save-button.html", { 'property': Property(**request.POST) })


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import SavedProperty
from comment.forms import CommentForm, ReportFormForm
from comment.models import Comment, CommentLike, ReplyLike
from profiles.models import Profile, BlockedUser
from api.google import google_street_view_api
from api.redfin import property_detail_api
from api.redfin.redfin_types import Property

from django_htmx.http import trigger_client_event


def property_detail_view(request, address:str='5663 Dunridge Drive, Pace FL 32571'):
    property = property_detail_api(address=address)
    # street_view_image = google_street_view_api(address=address)
    is_saved = False
    if request.user.is_authenticated:
        saved_qs = SavedProperty.objects.filter(Q(profile__user=request.user) & Q(property_id=property['propertyId']))
        is_saved = saved_qs.exists()
    return render(request, 'property/property-detail.html', {'property': property, 'is_saved': is_saved })

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

@login_required()
@require_http_methods(['POST'])
def toggle_property_saved(request, property_id: str):
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(Q(profile=profile) & Q(property_id=property_id))
    if not saved_qs.exists():
        SavedProperty.objects.create(
            profile=profile, 
            property_id=property_id,
            address=request.POST.get('address'),
            image=request.POST.get('image')
        )
        is_saved = True
    else:
        saved_qs.delete()
        is_saved = False
    property = Property(propertyId=property_id, address=request.POST.get('address'), photo=request.POST.get('image'))
    return render(request, "property/partials/detail-save-button.html", {'property': property, 'is_saved': is_saved  })


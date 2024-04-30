from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import CommentForm, ReplyForm
from .models import SavedProperty, Comment, Reply
from profiles.models import Profile 
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
    comment_list = Comment.objects.filter(property_id=property['propertyId']).order_by('-timestamp')
    context = {
        'property': property, 
        'is_saved': is_saved, 
        'form': CommentForm(),
        'comment_list': comment_list,
    }
    return render(request, 'property/property-detail.html', context)

@login_required()
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

@login_required()
@require_http_methods(['POST'])
def create_comment_view(request, property_id: str):
    profile = Profile.objects.get(user=request.user)
    comment = Comment.objects.create(
        profile=profile,
        property_id=property_id,
        text=request.POST.get('text')
    )
    return render(request, "property/partials/comment.html", {'comment': comment })

@login_required()
@require_http_methods(['GET'])
def edit_comment_view(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, profile=Profile.objects.get(user=request.user))
    form = CommentForm(instance=comment)
    return render(request, "property/partials/edit-comment-form.html", {'comment': comment, 'form': form})

@login_required()
@require_http_methods(['POST'])
def update_comment_view(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, profile=Profile.objects.get(user=request.user))
    comment.text = request.POST.get('text')
    comment.save()
    return render(request, "property/partials/comment.html", {'comment': comment })

@login_required()
@require_http_methods(['DELETE'])
def delete_comment_view(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, profile=Profile.objects.get(user=request.user))
    comment.delete()
    return HttpResponse(status=200)

@login_required()
@require_http_methods(['GET', 'POST'])
def create_reply_view(request, comment_id: int):
    profile = Profile.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        reply = Reply.objects.create(
            profile=profile,
            comment=comment,
            text=request.POST.get('text')
        )
        return render(request, "property/partials/reply.html", {'comment': comment, 'reply': reply })
    else:
        text_init: str = request.GET.get('text', '')
        reply = Reply(
            profile=profile,
            comment=comment,
            text=text_init
        )
        if request.GET.get('first'):
            return render(request, "property/partials/reply-form-first.html", {'comment': comment, 'reply': reply, 'form': ReplyForm() })
        return render(request, "property/partials/reply-form.html", {'comment': comment, 'reply': reply, 'form': ReplyForm(instance=reply)})

@login_required()
@require_http_methods(['POST'])
def edit_reply_view(request, comment_id: int, reply_id: int=0):
    profile = Profile.objects.get(user=request.user)
    if reply_id == 0:
        reply = Reply.objects(
            profile=profile,
            comment=Comment.objects.get(id=comment_id),
        )
        form = ReplyForm(instance=reply)
    else:
        reply = Reply.objects.get(id=reply_id, profile=profile)
        form = ReplyForm(instance=reply)
    return render(request, "property/partials/reply.html", {'reply': reply, 'form': form })

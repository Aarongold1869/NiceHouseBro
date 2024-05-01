from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import CommentForm, ReplyForm
from .models import SavedProperty, Comment, CommentLike, Reply
from profiles.models import Profile 
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
    comment_list = Comment.objects.filter(property_id=property['propertyId']).order_by('-timestamp')
    context = {
        'property': property, 
        'is_saved': is_saved, 
        'form': CommentForm(),
        'comment_list': comment_list,
        'comment_like_list': list(map(lambda x: x.comment.id, CommentLike.objects.filter(profile__user=request.user)))
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
@require_http_methods(['POST'])
def create_reply_view(request, comment_id: int):
    profile = Profile.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    reply = Reply.objects.create(
        profile=profile,
        comment=comment,
        text=request.POST.get('text')
    )
    response = render(request, "property/partials/reply.html", {'comment': comment, 'reply': reply })
    return trigger_client_event(response, f'update-reply-count-{comment.id}')

@login_required()
@require_http_methods(['GET'])
def edit_reply_view(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id, profile=Profile.objects.get(user=request.user))
    form = ReplyForm(instance=reply)
    context = {'comment': reply.comment, 'reply': reply, 'form': form }
    return render(request, "property/partials/edit-reply-form.html", context)

@login_required()
@require_http_methods(['POST'])
def update_reply_view(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id, profile=Profile.objects.get(user=request.user))
    reply.text = request.POST.get('text')
    reply.save()
    return render(request, "property/partials/reply.html", { 'comment': reply.comment, 'reply': reply })

@login_required()
@require_http_methods(['DELETE'])
def delete_reply_view(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id, profile=Profile.objects.get(user=request.user))
    comment = reply.comment
    reply.delete()
    response = HttpResponse(status=200)
    return trigger_client_event(response, f'update-reply-count-{comment.id}')
    
@login_required()
@require_http_methods(['GET'])
def get_reply_count(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    return HttpResponse(f'View {comment.reply_set.count()} replies', status=200)

@login_required()
@require_http_methods(['GET'])
def toggle_comment_like(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    comment_like_qs = CommentLike.objects.filter(Q(profile__user=request.user) & Q(comment=comment))
    count = comment_like_qs.count()
    if not comment_like_qs.exists():
        CommentLike.objects.create(
            profile=Profile.objects.get(user=request.user),
            comment=Comment.objects.get(id=comment_id)
        )
        count+=1
        liked=True
    else:
        comment_like_qs.delete()
        count-=1
        liked=False
    return render(request, "property/partials/comment-like-button.html", {'comment': comment, 'liked': liked })
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import CommentForm, ReplyForm
from .models import Comment, CommentLike, Reply, ReplyLike, ReportForm
from account.models import CustomUser
from profiles.models import Profile, BlockedUser

from django_htmx.http import trigger_client_event
import re

# Create your views here.
def format_tag_string(text: str)-> str:
    tags = re.findall(r'@(\w+)', text)
    for tag in tags:
        span_class = 'user-tag'
        user_qs = CustomUser.objects.filter(username=tag)
        if not user_qs.exists():
            span_class = 'failed-user-tag'
        text = text.replace(f'@{tag}', f'<span class="{span_class}">@{tag}</span>')
    return text

@require_http_methods(['GET'])
def format_user_tags(request):
    text = format_tag_string(request.GET.get('text'))
    return HttpResponse(text, status=200)

@login_required()
@require_http_methods(['POST'])
def create_comment_view(request, property_id: str):
    profile = Profile.objects.get(user=request.user)
    print(request.POST.get('url_path'))
    comment = Comment.objects.create(
        profile=profile,
        property_id=property_id,
        text=request.POST.get('text')
    )
    return render(request, "comment/comment.html", {'comment': comment })

@login_required()
@require_http_methods(['GET'])
def edit_comment_view(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, profile=Profile.objects.get(user=request.user))
    form = CommentForm(instance=comment)
    return render(request, "comment/edit-comment-form.html", {'comment': comment, 'form': form})

@login_required()
@require_http_methods(['POST'])
def update_comment_view(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, profile=Profile.objects.get(user=request.user))
    text = request.POST.get('text', comment.text)
    comment.text = text
    comment.save()
    p = f'<p id="comment-text-{comment.id}" class="card-text my-1 ms-1">{ format_tag_string(text) }</p>'
    return HttpResponse(p, status=200)

@login_required()
@require_http_methods(['DELETE'])
def delete_comment_view(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id, profile=Profile.objects.get(user=request.user))
    comment.delete()
    return HttpResponse(status=200)

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
    return render(request, "comment/comment-like-button.html", {'comment': comment, 'liked': liked })

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
    response = render(request, "comment/reply.html", { 'reply': reply })
    return trigger_client_event(response, f'update-reply-count-{comment.id}')

@login_required()
@require_http_methods(['GET'])
def edit_reply_view(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id, profile=Profile.objects.get(user=request.user))
    form = ReplyForm(instance=reply)
    context = { 'reply': reply, 'form': form }
    return render(request, "comment/edit-reply-form.html", context)

@login_required()
@require_http_methods(['POST'])
def update_reply_view(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id, profile=Profile.objects.get(user=request.user))
    text = request.POST.get('text', reply.text)
    reply.text = text
    reply.save()
    p = f'<p id="reply-text-{reply.id}" class="card-text my-1 ms-1">{ format_tag_string(text) }</p>'
    return HttpResponse(p, status=200)

@login_required()
@require_http_methods(['DELETE'])
def delete_reply_view(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id, profile=Profile.objects.get(user=request.user))
    comment = reply.comment
    reply.delete()
    response = HttpResponse(status=200)
    return trigger_client_event(response, f'update-reply-count-{comment.id}')
    
@require_http_methods(['GET'])
def get_reply_count(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    return HttpResponse(f'View {comment.reply_set.count()} replies', status=200)

@login_required()
@require_http_methods(['GET'])
def toggle_reply_like(request, reply_id: int):
    reply = Reply.objects.get(id=reply_id)
    reply_like_qs = ReplyLike.objects.filter(Q(profile__user=request.user) & Q(reply=reply))
    count = reply_like_qs.count()
    if not reply_like_qs.exists():
        ReplyLike.objects.create(
            profile=Profile.objects.get(user=request.user),
            reply=Reply.objects.get(id=reply_id)
        )
        count+=1
        liked=True
    else:
        reply_like_qs.delete()
        count-=1
        liked=False
    return render(request, "comment/reply-like-button.html", {'reply': reply, 'liked': liked })

@require_http_methods(['POST'])
def report_comment_view(request):
    data = request.POST
    ReportForm.objects.create(
        model=data.get('model'),
        object_id=data.get('object_id'),
        profile=Profile.objects.get(user=request.user),
        cause=data.get('cause'),
        reported_text=data.get('reported_text')
    )
    BlockedUser.objects.create(
        profile=Profile.objects.get(user=request.user),
        blocked_user=data.get('reported_user')
    )
    response = HttpResponse(status=200)
    return trigger_client_event(response, 'reload-comments')


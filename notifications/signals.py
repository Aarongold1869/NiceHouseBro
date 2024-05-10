from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver    
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from property.models import CommentLike

@receiver(post_save, sender=CommentLike)
def send_notifications_on_comment_like(sender, instance: CommentLike, created, **kwargs):
    if created:
        print('Comment Like Created')
        channel_layer = get_channel_layer()
        group_name = 'user-notifications'
        event = {
            'type': 'comment_liked',
            'header': f'@{instance.profile.user.username} liked your comment.',
            'message': f'"{instance.comment.text[:80]}..."',
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
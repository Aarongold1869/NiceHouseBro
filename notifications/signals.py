from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver    
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from comment.models import CommentLike, Reply
from notifications.models import Notification


@receiver(post_save, sender=CommentLike)
def send_notifications_on_comment_like(sender, instance: CommentLike, created, **kwargs):

    if created:
        if(instance.profile.user == instance.comment.profile.user):
            return
        notification = Notification.objects.create(
            user=instance.comment.profile.user,
            header=f'@{instance.profile.user.username} liked your comment.',
            message=f'"{instance.comment.text[:80]}..."',
        )
        channel_layer = get_channel_layer()
        group_name = f'user-notifications-{instance.comment.profile.user.id}'
        event = {
            'type': 'comment_interaction',
            'notification': notification
        }
        async_to_sync(channel_layer.group_send)(group_name, event)

@receiver(post_save, sender=Reply)
def send_notifications_on_reply(sender, instance: Reply, created, **kwargs):
    if created:
        if(instance.profile.user == instance.comment.profile.user):
            return
        notification = Notification.objects.create(
            user=instance.profile.user,
            header=f'@{instance.profile.user.username} replied to your comment.',
            message=f'"{instance.text[:80]}..."',
        )
        channel_layer = get_channel_layer()
        group_name = f'user-notifications-{instance.comment.profile.user.id}'
        event = {
            'type': 'comment_interaction',
            'notification': notification
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
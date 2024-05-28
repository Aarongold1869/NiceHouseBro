from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver    
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from agent.models import AgentContactForm
from comment.models import CommentLike, Reply
from property.models import SavedProperty
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

@receiver(post_save, sender=AgentContactForm)
def send_notifications_on_contact_form_submit(sender, instance: AgentContactForm, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.user,
            header=f'Contact Form Submitted.',
            message=f'Your contact form for {instance.address} was submitted successfully. An agent will be in touch soon.',
        )
        channel_layer = get_channel_layer()
        group_name = f'user-notifications-{instance.user.id}'
        event = {
            'type': 'comment_interaction',
            'notification': notification
        }
        async_to_sync(channel_layer.group_send)(group_name, event)

@receiver(post_save, sender=SavedProperty)
def send_notifications_on_property_saved(sender, instance: SavedProperty, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.profile.user,
            header=f'Property Saved.',
            message=f'You can view this property in the saved properties menu.',
        )
        channel_layer = get_channel_layer()
        group_name = f'user-notifications-{instance.profile.user.id}'
        event = {
            'type': 'comment_interaction',
            'notification': notification,
            'link': { 'href': '/profile/saved/', 'alt': 'View Saved Properties' }
        }
        async_to_sync(channel_layer.group_send)(group_name, event)

import os
@receiver(post_delete, sender=SavedProperty)
def auto_delete_file_on_delete(sender, instance: SavedProperty, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `SavedProperty` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path) and not 'default' in instance.image.path:
            os.remove(instance.image.path)
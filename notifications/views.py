from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Notification

import after_response
# Create your views here.

@after_response.enable
def set_notifications_read(notification_qs):
    for notification in notification_qs:
        notification.is_read = True
        notification.save()

def retreive_notification_view(request, *args, **kwargs):
    notification_qs = Notification.objects.filter(user=request.user)
    paginator = Paginator(notification_qs, 10) 
    page_number = int(request.GET.get("page"))
    paginated_qs = paginator.get_page(page_number)
    set_notifications_read.after_response(paginated_qs.object_list)
    return render(request, "notifications/partials/notification-list.html", {"notifications": paginated_qs })
from django.urls import path

from . import views

urlpatterns = [
    path("", views.retreive_notification_view, name="get-notifications"),
    path("delete/<int:id>", views.delete_notification_view, name="delete_notification")
]
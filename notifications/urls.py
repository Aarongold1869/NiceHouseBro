from django.urls import path

from . import views

urlpatterns = [
    path("", views.retreive_notification_view, name="get-notifications"),
]
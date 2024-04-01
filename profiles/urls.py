from django.urls import path

from . import views

urlpatterns = [
    path('locate/', views.locate_view, name='locate'),
]
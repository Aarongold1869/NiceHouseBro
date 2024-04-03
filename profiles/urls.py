from django.urls import path

from . import views

urlpatterns = [
    path('locate/', views.locate_view, name='locate'),
    path('saved/', views.saved_property_list_view, name='saved_property_list'),
    path('toggle-saved/<str:property_id>/', views.toggle_saved_property_archived, name='toggle_saved_profile'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]
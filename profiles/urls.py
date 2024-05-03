from django.urls import path

from . import views

urlpatterns = [
    path('locate/', views.locate_view, name='locate'),
    path('saved/', views.saved_property_list_view, name='saved_property_list'),
    path('update/', views.update_profile_view, name='update_profile'),
    path('update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('toggle-saved/<str:property_id>/', views.toggle_saved_property_archived, name='toggle_saved_profile'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('block-user/<int:blocked_user_id>/', views.block_user_view, name='block_user'),
]
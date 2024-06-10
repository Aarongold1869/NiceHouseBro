from django.urls import path

from . import views

urlpatterns = [
    path('user=<str:username>/', views.profile_view, name='profile'),
    path('locate/', views.locate_view, name='locate'),
    path('saved/', views.saved_property_list_view, name='saved_property_list'),
    path('update/<int:profile_id>/', views.update_profile_view, name='update_profile'),
    path('update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('block-user/<int:blocked_user_id>/', views.block_user_view, name='block_user'),

    path('validate-email/', views.validate_email, name='validate_email'),
    path('validate-phone-number/', views.validate_phone_number, name='validate_phone_number'),
    path('retrieve-new-formula/', views.retrieve_new_formula, name='retrieve_new_formula'),
]
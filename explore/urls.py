from django.urls import path

from . import views

urlpatterns = [
    path('', views.explore_view, name='explore'),
    path('search=<str:search_str>/', views.explore_view, name='explore-search'),
    # path('reverse/lng=<str:lng>lat=<str:lat>/', views.explore_view, name='explore-reverse-search'),
    path('get-card-image/', views.get_card_image_view, name='get_card_image'),
    path('explore-toggle-saved/', views.toggle_property_saved_explore_view, name='toggle_saved_explore'),
    path('filter/', views.filter_properties, name='filter_properties'),
] 
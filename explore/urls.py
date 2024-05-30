from django.urls import path

from . import views

urlpatterns = [
    path('', views.explore_view, name='explore'),
    path('search=<str:search_str>/', views.explore_view, name='explore-search'),
    path('filter/search=<str:search_str>&cap_rate=<str:cap_rate>/', views.explore_view_filtered, name='explore-cap-rate-filtered'),
    path('get-card-image/', views.get_card_image_view, name='get_card_image'),
] 
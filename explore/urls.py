from django.urls import path

from . import views

urlpatterns = [
    path('', views.explore_view_filtered, name='explore'),
    path('search=<str:search_str>/', views.explore_view_filtered, name='explore-search'),
    path('filter/search=<str:search_str>&cap-rate=<str:cap_rate>&min-price=<int:min_price>&max-price=<int:max_price>&bedrooms=<int:beds>&bathrooms=<int:baths>&min-sq-feet=<int:min_sq_ft>&max-sq-feet=<int:max_sq_ft>&lotSize-min=<int:min_lot>&lotSize-max=<int:max_lot>/', views.explore_view_filtered, name='explore_filtered'),
    path('get-card-image/', views.get_card_image_view, name='get_card_image'),
] 
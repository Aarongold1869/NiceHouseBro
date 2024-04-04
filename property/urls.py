from django.urls import path

from . import views

urlpatterns = [
    
    # Detail Views
    path('detail/<str:address>/', views.property_detail_view, name='property_detail'),
    path('detail-toggle-saved/<str:property_id>/', views.toggle_property_saved, name='toggle_saved'),

    # Explore Views
    path('get-card-image/', views.get_card_image_view, name='get_card_image'),
    path('get-explore-controls/<str:property_id>/', views.get_explore_controls_view, name='get_explore_controls'),
    path('explore-toggle-saved/<str:property_id>/', views.toggle_property_saved_explore_view, name='toggle_saved_explore'),
] 

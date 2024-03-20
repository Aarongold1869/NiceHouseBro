from django.urls import path

from . import views

urlpatterns = [
    path('<str:property_id>/', views.property_detail_view, name='property-detial'),
    path('toggle-desc-visible/<str:property_id>/<str:action>/', views.toggle_property_descripton, name='toggle_desc_visible'),
    path('toggle-saved/<str:property_id>/', views.toggle_property_saved, name='toggle_saved'),

    path('get-explore-controls/<str:property_id>/', views.get_explore_controls_view, name='get_explore_controls'),
    path('save-property-explore/<str:property_id>/', views.toggle_property_saved_explore_view, name='toggle_saved_explore'),
] 

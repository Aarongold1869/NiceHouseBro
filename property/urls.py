from django.urls import path

from . import views

urlpatterns = [
    path('<str:property_id>/', views.property_detail_view, name='property-detial'),
    path('toggle-desc-visible/<str:property_id>/<str:action>/', views.toggle_property_descripton, name='toggle_desc_visible'),
    path('toggle-saved/<str:property_id>/', views.toggle_property_saved, name='toggle_saved')
] 

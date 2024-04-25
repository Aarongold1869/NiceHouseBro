from django.urls import path

from . import views

urlpatterns = [
    path('detail/<str:address>/', views.property_detail_view, name='property_detail'),
    path('detail-toggle-saved/<str:property_id>/', views.toggle_property_saved, name='toggle_saved'),
] 

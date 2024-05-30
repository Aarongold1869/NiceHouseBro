from django.urls import path

from . import views

urlpatterns = [
    path('detail/state=<str:state>&city=<str:city>&address=<str:address>&zip=<int:zip>&id=<str:propertyId>/', views.property_detail_view, name='property_detail'),
    path('toggle-property-saved/', views.toggle_property_saved, name='toggle_property_saved'),
    path('get-comments/<str:property_id>/', views.retrieve_comment_section, name='get_comments'),
] 

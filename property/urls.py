from django.urls import path

from . import views

urlpatterns = [
    path('detail/<str:address>/', views.property_detail_view, name='property_detail'),
    path('detail-toggle-saved/<str:property_id>/', views.toggle_property_saved, name='toggle_saved'),
    path('create-comment/<str:property_id>/', views.create_comment_view, name='create_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment_view, name='edit_comment'),
    path('update-comment/<int:comment_id>/', views.update_comment_view, name='update_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment')
] 

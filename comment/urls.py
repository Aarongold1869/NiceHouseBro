from django.urls import path

from . import views

urlpatterns = [

    # Comments
    # path('get-comments/<str:property_id>/', views.retrieve_comment_section, name='get_comments'),
    path('create-comment/<str:property_id>/', views.create_comment_view, name='create_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment_view, name='edit_comment'),
    path('update-comment/<int:comment_id>/', views.update_comment_view, name='update_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('toggle-comment-like/<int:comment_id>/', views.toggle_comment_like, name='toggle_comment_like'),

    # Replies
    path('create-reply/<int:comment_id>/', views.create_reply_view, name='create_reply'),
    path('edit-reply/<int:reply_id>/', views.edit_reply_view, name='edit_reply'),
    path('update-reply/<int:reply_id>/', views.update_reply_view, name='update_reply'),
    path('delete-reply/<int:reply_id>/', views.delete_reply_view, name='delete_reply'),
    path('get-reply-count/<int:comment_id>/', views.get_reply_count, name='get_reply_count'),
    path('toggle-reply-like/<int:reply_id>/', views.toggle_reply_like, name='toggle_reply_like'),

    path('report-comment/', views.report_comment_view, name='report_comment'),
] 

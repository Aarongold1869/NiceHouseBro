from django.urls import path

from . import views

urlpatterns = [
    path('become-an-agent/', views.agent_splash_view, name='agent_splash'),
    path('register/', views.agent_register_view, name='agent_register'),
    path('dashboard/', views.agent_dashboard_view, name='agent_dashboard'),
    path('my-leads/', views.crm_view, name='agent_leads'),
]
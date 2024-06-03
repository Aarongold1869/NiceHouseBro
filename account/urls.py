from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("register/", views.register_step_1_view, name="register"),
    path("register/step-2/", views.register_step_2_view, name="register_step_2"),
    path("register/step-3/", views.register_step_3_view, name="register_step_3"),
]
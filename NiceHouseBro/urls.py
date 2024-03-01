from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from property import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('property/<int:property_id>/', views.property_detail_view, name='property-detial')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

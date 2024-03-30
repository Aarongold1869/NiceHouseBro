from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from property import views as property_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', property_views.home_view, name='home'),
    path('explore/', property_views.explore_view, name='explore'),
    path('explore/search=<str:search_str>/', property_views.explore_view, name='explore-search'),
    path('explore/reverse/lng=<str:lng>lat=<str:lat>/', property_views.explore_view, name='explore-search'),
    
    path('accounts/', include('account.urls')),
    path('property/', include('property.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

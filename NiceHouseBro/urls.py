from django.contrib import admin
from django.urls import path, include

from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('account/', include('account.urls')),
    path('agents/', include('agent.urls')),
    path('explore/', include('explore.urls')),
    path('profile/', include('profiles.urls')),
    path('property/', include('property.urls'))
]

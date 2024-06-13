from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import home_view, faq_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('faq/', faq_view, name='faq'),
    path('faq/<str:slug>/', faq_view, name='faq_slug'),
    path('account/', include('account.urls')),
    path('agent/', include('agent.urls')),
    path('comment/', include('comment.urls')),
    path('explore/', include('explore.urls')),
    path('notifications/', include('notifications.urls')),
    path('profile/', include('profiles.urls')),
    path('property/', include('property.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

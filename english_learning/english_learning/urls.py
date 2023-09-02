from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import (handler404, handler500)



urlpatterns = [
    path('admin/', admin.site.urls, name=admin),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('materials.urls')),
]

urlpatterns += i18n_patterns(
    path('materials/', include('materials.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'materials.views.page_not_found'
handler500 = 'materials.views.server_error'
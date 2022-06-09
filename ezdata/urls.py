
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
# from PV.admin import admin_site


urlpatterns = [
    path('', include('PV.urls')),
    path('admin/', admin.site.urls),
    # path('myadmin/', admin_site.urls, name='admin'),
    path('', include('users.urls')),
]

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL,
# document_root=settings.MEDIA_ROOT)

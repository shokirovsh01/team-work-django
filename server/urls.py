from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
    path('notifications/', include('notifications.urls')),
    path('accountsapp/', include('accountsapp.urls')),
    path('clinicapp/', include('clinicapp.urls')),
    path('reviewapp/', include('reviewapp.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
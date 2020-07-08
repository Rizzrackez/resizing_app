from django.contrib import admin
from resizing_app import settings
from django.conf.urls.static import static
from django.urls import path, include
from resizing_app.views import custom404


handler404 = custom404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_resizing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

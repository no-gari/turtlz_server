from django.contrib import admin
from django.conf import settings
from api.views import get_200, ads
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', get_200),
    path('app-ads.txt/', ads),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = f'{settings.SITE_NAME} Admin'
admin.site.site_title = f'{settings.SITE_NAME}'

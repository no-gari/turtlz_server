from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('commerce/', include('api.commerce.urls')),
    path('notification/', include('api.notification.urls')),
]

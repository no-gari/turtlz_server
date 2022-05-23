from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('magazine/', include('api.magazine.urls')),
    path('commerce/', include('api.commerce.urls')),
    path('community/', include('api.community.urls')),
    path('notification/', include('api.notification.urls')),
]

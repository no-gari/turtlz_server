from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('logger/', include('api.mypage.urls')),
    path('magazine/', include('api.magazine.urls')),
    path('commerce/', include('api.commerce.urls')),
    path('community/', include('api.community.urls')),
]

from django.urls import path

urlpatterns = [
    path('create/', ),
    path('list/', ),
    path('<str:order_number>/'),
]

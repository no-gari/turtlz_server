from django.urls import path
from api.notification.views import NotificationListView, NotificationDetailView

urlpatterns = [
    path('', NotificationListView.as_view()),
    path('<int:id>/', NotificationDetailView.as_view()),
]

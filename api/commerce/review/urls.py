from django.urls import path
from api.commerce.review.views import ReviewCreateAPIView, ReviewListView

urlpatterns = [
    path('create/', ReviewCreateAPIView.as_view()),
    path('', ReviewListView.as_view())
]

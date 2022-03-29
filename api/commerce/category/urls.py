from api.commerce.category.views import CategoryListAPIView
from django.urls import path


urlpatterns = [
    path('list/', CategoryListAPIView.as_view()),
]

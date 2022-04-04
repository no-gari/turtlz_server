from api.commerce.brand.views import BrandListView, BrandLikeView, BrandRetrieveView
from django.urls import path

urlpatterns = [
    path('', BrandListView.as_view()),
    path('<int:pk>/', BrandRetrieveView.as_view()),
    path('<int:pk>/like/', BrandLikeView.as_view()),
]

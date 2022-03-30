from api.commerce.product.views import ProductListView, ProductDetailView, ProductLikeView
from django.urls import path


urlpatterns = [
    path('', ProductListView.as_view()),
    path('', ProductListView.as_view()),
    path('<str:slug>/', ProductDetailView.as_view()),
    path('<str:slug>/like/', ProductLikeView.as_view()),
]

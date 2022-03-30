from django.urls import path
from api.commerce.product.views import ProductListView, ProductDetailView, ProductLikeView


urlpatterns = [
    path('', ProductListView.as_view()),
    path('<str:slug>/', ProductDetailView.as_view()),
    path('<str:slug>/like/', ProductLikeView.as_view()),
    path('product-options/<str:slug>/', )
]

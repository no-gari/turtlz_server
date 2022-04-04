from api.commerce.product.views import ProductListView, ProductDetailView, ProductLikeView, WishListProductView
from django.urls import path


urlpatterns = [
    path('', ProductListView.as_view()),
    path('like/', WishListProductView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
    path('<int:pk>/like/', ProductLikeView.as_view()),
]

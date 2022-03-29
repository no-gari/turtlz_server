from django.urls import path
from api.commerce.product.views import ProductListView, ProductDetailView, ProductLikeView


urlpatterns = [
    path('', ProductListView.as_view()),
    path('<int:id>/', ProductDetailView.as_view()),
    path('<int:id>/like/', ProductLikeView.as_view()),
]

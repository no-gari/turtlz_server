from django.urls import path
from api.commerce.product.views import ProductListView, ProductDetailView


urlpatterns = [
    path('list/', ProductListView.as_view()),
    path('detail/<int:id>', ProductDetailView.as_view()),
]

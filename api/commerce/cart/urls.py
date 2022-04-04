from api.commerce.cart.views import CartItemListCreateView, CartItemRetrieveUpdateDestroyView
from django.urls import path


urlpatterns = [
    path('', CartItemListCreateView.as_view()),
    path('update/', CartItemRetrieveUpdateDestroyView.as_view()),
]

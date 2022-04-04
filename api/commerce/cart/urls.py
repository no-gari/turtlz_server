from api.commerce.cart.views import CartItemCreateView, CartItemListView, CartItemRetrieveUpdateDestroyView
from django.urls import path


urlpatterns = [
    path('', CartItemListView.as_view()),
    path('add/', CartItemCreateView.as_view()),
    path('update/', CartItemRetrieveUpdateDestroyView.as_view()),
]

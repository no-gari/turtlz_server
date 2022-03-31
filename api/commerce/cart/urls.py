from django.urls import path
from api.commerce.cart.views import CartRetrieveUpdateDestroyView, CreateCartItemView


urlpatterns = [
    path('', CartRetrieveUpdateDestroyView),
    path('add/', CreateCartItemView),
]

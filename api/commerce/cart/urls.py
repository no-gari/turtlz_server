from api.commerce.cart.views import CartRetrieveUpdateDestroyView, CreateCartItemView
from django.urls import path


urlpatterns = [
    path('', CartRetrieveUpdateDestroyView.as_view()),
    path('add/', CreateCartItemView.as_view()),
]

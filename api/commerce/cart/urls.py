from api.commerce.cart.views import CartRetrieveView, CreateCartItemView, DestroyCartItemView, UpdateCartItemView
from django.urls import path


urlpatterns = [
    path('', CartRetrieveView.as_view()),
    path('add/', CreateCartItemView.as_view()),
    path('update/', UpdateCartItemView.as_view()),
    path('destroy/', DestroyCartItemView.as_view()),
]

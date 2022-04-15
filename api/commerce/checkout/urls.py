from django.urls import path
from api.commerce.checkout.views import CheckoutView

urlpatterns = [
    path('', CheckoutView.as_view()),
]

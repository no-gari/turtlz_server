from django.urls import path
from api.commerce.checkout.views import CheckoutRetrieveView

urlpatterns = [
    path('', CheckoutRetrieveView.as_view()),
]

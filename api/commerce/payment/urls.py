from django.urls import path

from api.commerce.payment.views import PaymentCreateView, PaymentCallbackView

urlpatterns = [
    path('', PaymentCreateView.as_view()),
    path('callback/', PaymentCallbackView.as_view()),
]

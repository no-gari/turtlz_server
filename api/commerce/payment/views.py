from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

# from api.payment.serializers import PaymentCreateSerializer, PaymentCallbackSerializer


class PaymentCreateView(CreateAPIView):
    # serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]


class PaymentCallbackView(CreateAPIView):
    # serializer_class = PaymentCallbackSerializer
    pass
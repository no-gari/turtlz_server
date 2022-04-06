from api.commerce.checkout.serializers import CheckoutSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, GenericAPIView


class CheckoutRetrieveView(GenericAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        pass

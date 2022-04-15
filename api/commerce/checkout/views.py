from api.commerce.product.models import ProductVariant
from api.commerce.checkout.serializers import CheckoutSerializer
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from json import loads, dumps


class CheckoutView(GenericAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        checkout_list = []
        for check_out_item in request.data.get('check_out_items'):
            serialized_item = loads(dumps(self.get_serializer(ProductVariant.objects.get(id=check_out_item.get('product_variant'))).data))
            checkout_list.append(serialized_item)
        a=1
        b=2


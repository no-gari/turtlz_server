from api.commerce.checkout.serializers import CheckoutSerializer, ShippingrRequestSerializers
from api.commerce.checkout.models import ShippingRequest
from api.commerce.product.models import ProductVariant
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from api.utils import list_converter
from json import loads, dumps


class CheckoutView(GenericAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        product_variants = [data['product_variant'] for data in request.data['check_out_items']]
        serialized_items = loads(dumps(self.get_serializer(ProductVariant.objects.prefetch_related('product').filter(id__in=product_variants), many=True).data))
        request = ShippingrRequestSerializers(ShippingRequest.objects.all(), many=True).data
        product_list = list_converter(serialized_items)
        is_cart = request.data['is_cart']
        return Response({'isCart': is_cart, 'checkoutList': product_list, 'request': request}, status=HTTP_200_OK)

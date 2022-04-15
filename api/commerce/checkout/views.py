from api.commerce.checkout.serializers import CheckoutSerializer
from api.commerce.product.models import ProductVariant
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.utils import list_converter
from rest_framework import status
from json import loads, dumps


class CheckoutView(GenericAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        product_variants = [data['product_variant'] for data in request.data['check_out_items']]
        serialized_items = loads(dumps(self.get_serializer(ProductVariant.objects.prefetch_related('product').filter(id__in=product_variants), many=True).data))
        product_list = list_converter(serialized_items)
        return Response(product_list, status=status.HTTP_200_OK)

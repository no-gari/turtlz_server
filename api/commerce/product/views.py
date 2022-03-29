from api.commerce.product.models import Product
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_object(self):
        return Product.objects.get(id=self.kwargs['id'])

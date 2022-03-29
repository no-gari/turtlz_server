from api.commerce.product.models import Product
from rest_framework.pagination import PageNumberPagination
from api.commerce.product.filtersets import ProductFilterSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer, ProductLikeSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductListView(ListAPIView):
    queryset = Product.objects.prefetch_related('wish_product').all()
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    filter_class = ProductFilterSet
    permission_classes = [AllowAny]


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_object(self):
        return Product.objects.get(id=self.kwargs['id'])


class ProductLikeView(UpdateAPIView):
    queryset = Product.objects.prefetch_related('wish_product').all()
    serializer_class = ProductLikeSerializer
    permission_classes = [IsAuthenticated]

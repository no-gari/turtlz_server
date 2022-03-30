from rest_framework.pagination import PageNumberPagination
from api.commerce.product.filtersets import ProductFilterSet
from api.commerce.product.models import Product, ProductVariant
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer, \
    ProductLikeSerializer, ProductVariantSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 10


class ProductListView(ListAPIView):
    queryset = Product.objects.prefetch_related('wish_product').all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductListSerializer
    filter_class = ProductFilterSet
    permission_classes = [AllowAny]


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_object(self):
        return Product.objects.get(slug=self.kwargs['slug'])


class ProductVariantView(RetrieveAPIView):
    serializer_class = ProductVariantSerializer
    pagination_class = None

    def get_queryset(self):
        return ProductVariant.objects.filter(product_option__slug=self.kwargs['slug'])


class ProductLikeView(UpdateAPIView):
    queryset = Product.objects.prefetch_related('wish_product').all()
    serializer_class = ProductLikeSerializer
    permission_classes = [IsAuthenticated]

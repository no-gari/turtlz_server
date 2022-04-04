from api.commerce.product.models import Product
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from api.commerce.product.filtersets import ProductFilterSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from api.commerce.product.serializers import ProductListSerializer, ProductDetailSerializer, ProductLikeSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 10


class ProductListView(ListAPIView):
    queryset = Product.objects.prefetch_related('wish_product').filter(is_active=True)
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['hits', 'discount_price']
    serializer_class = ProductListSerializer
    filter_class = ProductFilterSet
    permission_classes = [AllowAny]


class WishListProductView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        wishlist = self.request.user.wish_product.all()
        return wishlist


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Product.objects.prefetch_related('wish_product').get(id=self.kwargs['pk'])


class ProductLikeView(UpdateAPIView):
    queryset = Product.objects.prefetch_related('wish_product').all()
    serializer_class = ProductLikeSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put']

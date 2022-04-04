from api.commerce.brand.serializers import BrandRetrieveSerializer, BrandListSerializer, BrandLikeSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.commerce.brand.models import Brand


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 10


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]


class BrandRetrieveView(RetrieveAPIView):
    serializer_class = BrandRetrieveSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Brand.objects.prefetch_related('wish_brand').get(id=self.kwargs['pk'])


class BrandLikeView(UpdateAPIView):
    queryset = Brand.objects.prefetch_related('wish_brand').all()
    serializer_class = BrandLikeSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put']

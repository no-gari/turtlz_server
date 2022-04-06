from api.commerce.brand.serializers import BrandRetrieveSerializer, BrandListSerializer, BrandLikeSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.utils import StandardResultsSetPagination
from api.commerce.brand.models import Brand


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


class WishListBrandView(ListAPIView):
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        wishlist = self.request.user.wish_brand.all()
        return wishlist

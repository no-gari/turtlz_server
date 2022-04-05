from api.commerce.coupon.models import Coupon, CouponUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, ListCreateAPIView
from api.commerce.coupon.serializers import CouponSerializer, CouponUserSerializer


class CouponListView(ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Coupon.objects.filter(brand_id=self.kwargs['id'])


class CouponUserListCreateView(ListCreateAPIView):
    serializer_class = CouponUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return CouponUser.objects.filter(user=self.request.user)

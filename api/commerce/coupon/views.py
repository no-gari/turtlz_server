from api.commerce.coupon.models import Coupon, CouponUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from api.commerce.coupon.serializers import CouponSerializer, CouponUserSerializer, CouponUserCreateSerializer


class CouponListView(ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Coupon.objects.filter(brand_id=self.request.POST['id'])


class CouponUserListView(ListAPIView):
    serializer_class = CouponUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return CouponUser.objects.filter(user=self.request.user)


class CouponUserCreateView(CreateAPIView):
    serializer_class = CouponUserCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return CouponUser.objects.filter(user=self.request.user)

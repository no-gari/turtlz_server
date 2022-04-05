from rest_framework import serializers
from api.commerce.coupon.models import Coupon, CouponUser


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['brand', 'name', 'discount_price', 'expire_date']


class CouponUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponUser
        fields = ['']
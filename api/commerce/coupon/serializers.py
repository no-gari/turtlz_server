from rest_framework import serializers
from rest_framework.validators import ValidationError
from api.commerce.coupon.models import Coupon, CouponUser


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'brand', 'name', 'discount_price', 'expire_date']
        read_only_fields = ['id', 'name', 'discount_price', 'expire_date']


class CouponUserSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer()

    class Meta:
        model = CouponUser
        fields = ['coupon', 'used']


class CouponUserCreateSerializer(serializers.Serializer):
    coupon = serializers.CharField(write_only=True)

    def create(self, validated_data):
        coupon_user = CouponUser.objects.create(user=self.context['request'].user, coupon_id=validated_data['coupon'])
        coupon_user.save()
        return coupon_user

    def validate(self, obj):
        coupon = Coupon.objects.get(id=obj['coupon'])
        if coupon.coupon_limit is not None and coupon.coupon_limit == 0:
            raise ValidationError({'error': '이미 소진된 쿠폰입니다.'})
        return super().validate(obj)

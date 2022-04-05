from rest_framework import serializers
from api.commerce.coupon.models import Coupon, CouponUser


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'brand', 'name', 'discount_price', 'expire_date']
        read_only_fields = ['id', 'name', 'discount_price', 'expire_date']


class CouponUserSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(source='coupon')

    class Meta:
        model = CouponUser
        fields = ['coupon', 'used']

    def create(self, validated_data):
        coupon = validated_data['coupon']
        coupon_user = self.Meta.model.objects.create(user=self.context['request'].user, coupon_id=coupon['id'])
        coupon_user.save()
        return coupon_user

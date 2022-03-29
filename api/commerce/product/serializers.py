from api.commerce.product.models import Product, ProductVariant
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        read_only_fields = ['name', 'slug', 'brand', 'banner_img', 'org_price', 'discount_price', 'is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False


class ProductDetailSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        read_only_fields = ['name', 'slug', 'brand', 'banner_img', 'org_price', 'discount_price', 'is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False

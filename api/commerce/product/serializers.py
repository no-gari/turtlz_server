from api.commerce.product.models import Product, ProductVariant
from rest_framework import serializers


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'banner_img', 'discount_price']


class ProductListSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)
    brand_name = serializers.CharField(read_only=True, source="brand.name")

    class Meta:
        model = Product
        fields = ['name', 'brand_name', 'banner_img', 'org_price', 'discount_price', 'is_like']
        read_only_fields = ['name', 'brand_name', 'banner_img', 'org_price', 'discount_price', 'is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.wish_product.all()
        else:
            return False


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'sold_out']
        read_only_fields = ['id', 'name', 'sold_out']


class ProductDetailSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)
    product_variant = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'banner_img', 'summary', 'description', 'product_variant', 'video',
                  'org_price', 'discount_price', 'is_like', 'sold_out']
        read_only_fields = ['id', 'name', 'brand', 'banner_img', 'summary', 'description', 'product_variant',
                            'video', 'org_price', 'discount_price', 'is_like', 'sold_out']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.wish_product.all()
        else:
            return False


class ProductLikeSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.wish_product.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.wish_product.all():
            instance.wish_product.remove(user)
        else:
            instance.wish_product.add(user)
        return instance

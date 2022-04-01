from api.commerce.product.models import Product, ProductVariant
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)
    brand_name = serializers.CharField(read_only=True, source="brand.name")

    class Meta:
        model = Product
        fields = ['name', 'slug', 'brand_name', 'banner_img', 'org_price', 'discount_price', 'is_like']
        read_only_fields = ['name', 'slug', 'brand_name', 'banner_img', 'org_price', 'discount_price', 'is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['slug', 'name', 'restrict_quantity', 'quantity']
        read_only_fields = ['slug', 'name', 'restrict_quantity', 'quantity']


class ProductDetailSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)
    product_variant = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'brand', 'banner_img', 'summary', 'description', 'product_variant', 'video',
                  'org_price', 'discount_price', 'is_like', 'restrict_quantity', 'quantity']
        read_only_fields = ['name', 'slug', 'brand', 'banner_img', 'summary', 'description', 'product_variant',
                            'video', 'org_price', 'discount_price', 'is_like', 'restrict_quantity', 'quantity']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
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
            return user in obj.like_user_set.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.like_user_set.all():
            instance.like_user_set.remove(user)
        else:
            instance.like_user_set.add(user)
        return instance

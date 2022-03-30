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


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        read_only_fields = ['slug', 'name', 'restrict_quantity', 'quantity']


class ProductDetailSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)
    product_option = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        read_only_fields = ['name', 'slug', 'brand', 'banner_img', 'summary', 'description', 'product_option',
                            'video', 'org_price', 'discount_price', 'is_like', 'restrict_quantity', 'quantity']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product_option'] = ProductOptionSerializer(instance.product_option).data
        return response

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

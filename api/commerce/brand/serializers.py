from api.commerce.brand.models import Brand
from rest_framework import serializers


class SimpleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'least_price', 'shipping_price']


class BrandRetrieveSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['is_like', 'wish_brand', 'brand_banner', 'thumbnail_image', 'description']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.wish_brand.all()
        else:
            return False


class BrandListSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        fields = ['is_like', 'thumbnail_image', 'name']


class BrandLikeSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.wish_brand.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.wish_brand.all():
            instance.wish_brand.remove(user)
        else:
            instance.wish_brand.add(user)
        return instance

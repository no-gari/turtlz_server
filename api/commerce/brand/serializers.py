from rest_framework import serializers
from api.commerce.brand.models import Brand


class SimpleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'least_price', 'shipping_price']


class BrandRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['wish_brand', 'brand_banner', 'thumbnail_image', 'description']


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['thumbnail_image', 'name']

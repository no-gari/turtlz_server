from rest_framework import serializers
from api.commerce.brand.models import Brand


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
            return user in obj.like_users.all()
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

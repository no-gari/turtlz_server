from api.magazine.models import Magazines, MagazineComments, Catalog
from api.commerce.product.serializers import ProductListSerializer
from rest_framework.validators import ValidationError
from api.clayful_client import ClayfulProductClient
from django.utils.html import strip_tags
from rest_framework import serializers


class MagazinesListSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['banner_image', 'id', 'content', 'title', 'subtitle']

    def get_content(self, value):
        content = strip_tags(value.content)
        return content


class MagazineRetrieveSerializer(serializers.ModelSerializer):
    like_user_count = serializers.IntegerField(source='like_users.count')
    total_comments = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['banner_image', 'id', 'content', 'title', 'hits', 'created_at', 'updated_at',
                  'comments_banned', 'like_user_count', 'total_comments', 'products', 'subtitle', 'magazine_url']

    def get_total_comments(self, obj):
        total_comments = obj.magazine_comments.count()
        return total_comments

    def get_products(self, obj):
        try:
            collection_id = obj.collection
            if collection_id is None:
                return []
            clayful_product_client = ClayfulProductClient()
            products_data = clayful_product_client.list_products(collection=collection_id).data
            serializer = ProductListSerializer(products_data, many=True)
            return serializer.data
        except Exception:
            return ValidationError({'error_msg': '매거진을 불러오지 못했습니다.'})


class MagazineLikeSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['is_like']

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.like_users.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            return ValidationError({'error_msg': '좋아요를 누르려면 로그인 해야 합니다.'})
        if user in instance.like_users.all():
            instance.like_users.remove(user)
        else:
            instance.like_users.add(user)
        return instance


class MagazineScrapUpdateSerializer(serializers.ModelSerializer):
    is_scrapped = serializers.SerializerMethodField()

    class Meta:
        model = Magazines
        fields = ['is_scrapped']

    def get_is_scrapped(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user in obj.scrapped_users.all()
        else:
            return False

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            return ValidationError({'error_msg': '스크랩을 하려면 로그인 해야 합니다.'})
        if user in instance.scrapped_users.all():
            instance.scrapped_users.remove(user)
        else:
            instance.scrapped_users.add(user)
        return instance


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class MagazineReviewsListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    reply = RecursiveSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = MagazineComments
        fields = ['id', 'content', 'created_at', 'updated_at', 'magazines', 'user', 'name', 'parent', 'reply']

    def get_name(self, obj):
        return obj.user.name

    def get_user(self, obj):
        return obj.user.email


class MagazineReviewCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    user = serializers.CharField(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = MagazineComments
        fields = ['id', 'content', 'created_at', 'updated_at', 'magazines', 'user', 'name', 'parent']

    def get_name(self, obj):
        return obj.user.name


class MagazineReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = ['id', 'content']


class MagazineReviewDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineComments
        fields = ['id']


class CatalogSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = ['id', 'banner_image', 'title', 'description', 'products']

    def get_products(self, obj):
        clf_product_client = ClayfulProductClient()
        products = clf_product_client.list_products(page=1, collection=obj.collection).data
        serialized_products = ProductListSerializer(products, many=True).data[:3]
        return serialized_products


class CatalogDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = ['id', 'banner_image', 'title', 'description', 'products']

    def get_products(self, obj):
        clf_product_client = ClayfulProductClient()
        products = clf_product_client.list_products(page=1, collection=obj.collection).data
        serialized_products = ProductListSerializer(products, many=True).data
        return serialized_products

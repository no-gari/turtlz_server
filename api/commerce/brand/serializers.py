from api.commerce.product.serializers import ProductListSerializer
from api.magazine.serializers import MagazinesListSerializer
from api.clayful_client import ClayfulProductClient
from api.magazine.models import Magazines
from django.utils.html import strip_tags
from rest_framework import serializers


class BrandListRetrieveSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    def get_logo(self, value):
        return value['logo']['url']


class BrandRetrieveSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    # description = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    # logo = serializers.SerializerMethodField(read_only=True)
    magazines = serializers.SerializerMethodField(required=False)
    products = serializers.SerializerMethodField(required=False)

    def get_description(self, value):
        return strip_tags(value['description'])

    def get_logo(self, value):
        return value['logo']['url']

    def get_magazines(self, value):
        try:
            magazines = Magazines.objects.filter(brand=value['_id'])
            magazine_data = MagazinesListSerializer(magazines, many=True).data
            return magazine_data
        except:
            return []

    def get_products(self, value):
        clayful_product_client = ClayfulProductClient()
        try:
            products = clayful_product_client.get_related_products(brand_id=value['_id'])
            product_data = ProductListSerializer(products.data, many=True).data
            return product_data
        except:
            return []


class BrandDetailMagazineSerializer(serializers.Serializer):
    _id = serializers.SerializerMethodField(read_only=True, required=False)
    description = serializers.SerializerMethodField(read_only=True, required=False)
    name = serializers.SerializerMethodField(read_only=True, required=False)
    logo = serializers.SerializerMethodField(read_only=True, required=False)
    magazines = serializers.SerializerMethodField(read_only=True, required=False)
    products = serializers.SerializerMethodField(read_only=True, required=False)

    def get__id(self, value):
        return None

    def get_description(self, value):
        return None

    def get_name(self, value):
        return None

    def get_logo(self, value):
        return None

    def get_magazines(self, value):
        try:
            magazine_data = MagazinesListSerializer(value, many=True).data
            return magazine_data
        except:
            return []

    def get_products(self, value):
        return None

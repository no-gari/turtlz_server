from rest_framework import serializers
from api.commerce.product.models import ProductVariant
from api.commerce.brand.serializers import SimpleBrandSerializer
from api.commerce.product.serializers import SimpleProductSerializer


class CheckoutSerializer(serializers.Serializer):
    brand = SimpleBrandSerializer(read_only=True, source='product.brand')
    product = SimpleProductSerializer(read_only=True)
    variant_name = serializers.SerializerMethodField()
    variant_id = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['brand', 'product', 'variant_name', 'variant_id', 'quantity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        brand = data.pop('brand', None)
        for key, value in brand.items():
            data['brand_{key}'.format(key=key)] = value
        return data

    def get_variant_name(self, instance):
        return instance.name

    def get_variant_id(self, instance):
        return instance.id

    def get_quantity(self, obj):
        a=1
        return obj['quantity']

from rest_framework import serializers
from api.commerce.cart.models import CartItem
from api.commerce.brand.serializers import SimpleBrandSerializer
from api.commerce.product.serializers import SimpleProductSerializer


# 카트에 상품 추가, 수정, 삭제를 위해 id, quantity 만 받는다.
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_variant', 'quantity']

    def update(self, instance, validated_data):
        quantity = validated_data['quantity']
        product_variant = validated_data['product_variant']
        cart_item = self.Meta.model.objects.get(user=self.context['request'].user, product_variant=product_variant)
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item


# 실제 추가하는 serializer. 다수의 상품을 한 번에 추가하기 위해 many=true 사용함.
class CartItemCreateSerializer(serializers.Serializer):
    cart_items = CartItemSerializer(many=True, write_only=True)

    def create(self, validated_data):
        instances = []
        for item in validated_data['cart_items']:
            check_item_result = self.check_item(item)
            if check_item_result is True:
                new_cart_item = CartItem.objects.create(
                    user=self.context['request'].user,
                    product_variant=item['product_variant'],
                    quantity=item['quantity'],
                )
                new_cart_item.save()
                instances.append(new_cart_item)
            instances.append(check_item_result)
        return instances[0]

    def check_item(self, item):
        cart_check = CartItem.objects.filter(
            product_variant=item['product_variant'],
            user=self.context['request'].user,
        )
        if cart_check.exists():
            cart_item = cart_check.first()
            cart_item.quantity += item['quantity']
            cart_item.save()
            return cart_item
        return True


# 실제 카트에서 보여지는 화면을 위한 serializer. 카트에 담은 상품 하나하나를 각각 serialize 한다.
class CartProductSerializer(serializers.Serializer):
    brand = SimpleBrandSerializer(read_only=True, source='product_variant.product.brand')
    product = SimpleProductSerializer(read_only=True, source='product_variant.product')
    variant_name = serializers.CharField(source='product_variant.name')
    variant_id = serializers.CharField(source='product_variant.id')
    quantity = serializers.CharField()

    class Meta:
        model = CartItem
        fields = ['brand', 'product', 'variant_name', 'variant_id', 'quantity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        brand = data.pop('brand', None)
        for key, value in brand.items():
            data['brand_{key}'.format(key=key)] = value
        return data

from rest_framework import serializers
from api.commerce.cart.models import Cart, CartItem
from api.commerce.brand.serializers import SimpleBrandSerializer
from api.commerce.product.serializers import SimpleProductSerializer


# 카트에 상품 추가를 위해 variant, quantity 만 받는다.
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_variant', 'quantity']


# 실제 추가하는 serializer. 다수의 상품을 한 번에 추가하기 위해 many=true 사용함.
class CartItemCreateSerializer(serializers.Serializer):
    cart_items = CartItemSerializer(many=True, write_only=True)

    def get_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.context['request'].user)
        return cart

    def create(self, validated_data):
        cart = self.get_cart()
        for item in validated_data['cart_items']:
            if self.check_item(item):
                new_cart_item = CartItem.objects.create(
                    cart=cart,
                    product_variant=item['product_variant'],
                    quantity=item['quantity'],
                )
                new_cart_item.save()
        return cart

    def check_item(self, item):
        cart_check = CartItem.objects.select_related('cart').filter(
            product_variant=item['product_variant'],
            cart__user=self.context['request'].user,
        )
        if cart_check.exists():
            cart_item = cart_check.first()
            cart_item.quantity += item['quantity']
            cart_item.save()
            return False
        return True


# 실제 카트에서 보여지는 화면을 위한 serializer. 카트에 담은 상품 하나하나를 각각 serialize 한다.
class CartProductSerializer(serializers.Serializer):
    brand = SimpleBrandSerializer(read_only=True, source='product_variant.product.brand')
    product = SimpleProductSerializer(read_only=True, source='product_variant.product')
    variant_name = serializers.CharField(source='product_variant.name')
    variant_slug = serializers.CharField(source='product_variant.slug')
    quantity = serializers.CharField()

    class Meta:
        model = CartItem
        fields = ['brand', 'product', 'variant_name', 'variant_slug', 'quantity']


# 마지막으로 카트에 보내는 역할.
class CartSerializer(serializers.ModelSerializer):
    cart_item_set = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['cart_item_set']

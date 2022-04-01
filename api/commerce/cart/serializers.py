from rest_framework import serializers
from api.commerce.cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    cart_item_set = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'cart_item_set']

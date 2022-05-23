from api.commerce.order.models import OrderItem, Order
from rest_framework import serializers
import string
import random


class OrderItemCreateSerializer(serializers.Serializer):
    def create(self, validated_data):
        order_number = ''.join([random.choice(string.ascii_lowercase) for i in range(32)])
        order = Order.objects.create(order_number=order_number)

        # 최종 금액
        # 배송지
        # 최종 할인 금액 검증

    def validate(self, attrs):
        pass


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_item_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

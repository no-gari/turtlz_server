from api.commerce.review.models import Reviews
from rest_framework import serializers
from api.commerce.order.serializers import OrderItemSerializer


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        exclude = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        review = self.Meta.model.objects.create(
            user=user,
            order_item_id=validated_data['order_item'],
            rates=validated_data['rates'],
            title=validated_data['title'],
            body=validated_data['body'],
            image=validated_data['image'],
        )
        review.save()
        return review


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source='user.profile.nickname')
    order_item = serializers.CharField(read_only=True, source='order_item.product_variant.name')

    class Meta:
        model = Reviews
        fields = ['user', 'order_item', 'rates', 'title', 'body', 'image']

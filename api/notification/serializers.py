from rest_framework import serializers
from api.notification.models import Notification, NotificationComments


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['url']


class NotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# class NotificationReviewCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NotificationComments
#         fields = '__all__'

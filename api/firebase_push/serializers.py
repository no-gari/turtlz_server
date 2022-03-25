from api.firebase_push.models import PushToken
from rest_framework import serializers


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = (
            'id',
            'token',
            'user',
        )

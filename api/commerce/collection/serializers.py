from rest_framework import serializers
from .models import CollectionModel


class CollectionRetrieveSerializers(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)

    def get_thumbnail(self, value):
        return value['thumbnail']['url']


class PopUpCollectionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollectionModel
        fields = '__all__'

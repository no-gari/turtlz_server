from api.commerce.category.models import Category
from rest_framework import serializers


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'parent', 'slug', 'category')

    def get_category(self, instance):
        serializer = self.__class__(instance.category, many=True)
        serializer.bind('', self)
        return serializer.data

from api.commerce.category.models import Category
from rest_framework import serializers


class CategoryListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'parent', 'slug', 'category')

    def get_category(self, instance):
        serializer = self.__class__(instance.category, many=True)
        serializer.bind('', self)
        return serializer.data

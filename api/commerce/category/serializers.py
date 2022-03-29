from api.commerce.category.models import Category
from rest_framework import serializers


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

from api.commerce.category.serializers import CategoryListSerializer
from api.commerce.category.models import Category
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

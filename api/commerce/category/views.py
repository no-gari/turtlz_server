from api.commerce.category.serializers import CategoryListSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

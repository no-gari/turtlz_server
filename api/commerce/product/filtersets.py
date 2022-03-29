import django_filters
from api.commerce.product.models import Product


class ProductFilterSet(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['brand', 'is_active']

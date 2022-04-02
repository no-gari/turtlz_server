from api.commerce.product.models import Product
import django_filters


class ProductFilterSet(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'brand': ['exact'],
            'category': ['exact'],
            'discount_price': ['lt', 'gt'],
        }

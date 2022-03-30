from api.commerce.product.models import Product
import django_filters


class ProductFilterSet(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'brand__slug': ['exact'],
            'category__slug': ['exact'],
            'discount_price': ['lt', 'gt'],
        }

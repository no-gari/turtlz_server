from django.contrib import admin
from api.commerce.brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ['manager', 'slug', 'name', 'brand_banner', 'thumbnail_image', 'description', 'least_price', 'shipping_price']
    readonly_fields = ['slug']

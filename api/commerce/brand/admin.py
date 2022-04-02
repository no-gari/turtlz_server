from django.contrib import admin
from api.commerce.brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ['manager', 'name', 'brand_banner', 'thumbnail_image', 'description', 'least_price', 'shipping_price']

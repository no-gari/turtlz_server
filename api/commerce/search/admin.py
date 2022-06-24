from django.contrib import admin
from .models import SearchKeywords
from ..customer.models import ShippingRequest


@admin.register(SearchKeywords)
class SearchKeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(ShippingRequest)
class ShippingRequestAdmin(admin.ModelAdmin):
    pass

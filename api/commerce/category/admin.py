from django.contrib import admin
from api.commerce.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent', 'slug']
    readonly_fields = ['slug']

from django.contrib import admin
from api.commerce.cart.models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass

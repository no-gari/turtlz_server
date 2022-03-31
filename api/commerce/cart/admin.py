from django.contrib import admin
from api.commerce.cart.models import Cart, CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

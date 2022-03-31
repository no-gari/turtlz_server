from django.contrib import admin
from api.commerce.cart.models import Cart, CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    fields = ['product', 'quantity']
    readonly_fields = ['product', 'quantity']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ['user', 'cart_item']
    readonly_fields = ['user', 'cart_item']

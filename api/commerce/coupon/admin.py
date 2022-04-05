from django.contrib import admin
from api.commerce.coupon.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    fields = ['brand', 'name', 'coupon_limit', 'discount_price', 'expire_date']

from django.utils.translation import gettext_lazy as _
from api.user.models import User
from django.db import models


# class Checkout(models.Model):
#     created = models.DateTimeField(auto_now_add=True, verbose_name=_("생성일자"),)
#     last_change = models.DateTimeField(auto_now=True, verbose_name=_("수정일자"),)
#     user = models.ForeignKey(
#         User,
#         blank=True,
#         null=True,
#         related_name="checkout",
#         on_delete=models.CASCADE,
#     )
#     slug = models.SlugField(verbose_name=_("카테고리 슬러그"), max_length=255)
#     email = models.EmailField(blank=True, null=True)
#     phone = models.CharField(blank=True, null=True)
#     billing_address = models.ForeignKey(
#         "account.Address",
#         related_name="+",
#         editable=False,
#         null=True,
#         on_delete=models.SET_NULL,
#     )
#     shipping_address = models.ForeignKey(
#         "account.Address",
#         related_name="+",
#         editable=False,
#         null=True,
#         on_delete=models.SET_NULL,
#     )
#     shipping_method = models.ForeignKey(
#         ShippingMethod,
#         blank=True,
#         null=True,
#         related_name="checkouts",
#         on_delete=models.SET_NULL,
#     )
#     collection_point = models.ForeignKey(
#         "warehouse.Warehouse",
#         blank=True,
#         null=True,
#         related_name="checkouts",
#         on_delete=models.SET_NULL,
#     )
#     note = models.TextField(blank=True, default="")
#     discount_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         default=0,
#     )
#     discount = MoneyField(amount_field="discount_amount", currency_field="currency")
#     discount_name = models.CharField(max_length=255, blank=True, null=True)
#     translated_discount_name = models.CharField(max_length=255, blank=True, null=True)
#     voucher_code = models.CharField(max_length=12, blank=True, null=True)
#     gift_cards = models.ManyToManyField(GiftCard, blank=True, related_name="checkouts")
#     redirect_url = models.URLField(blank=True, null=True)
#     tracking_code = models.CharField(max_length=255, blank=True, null=True)
#     language_code = models.CharField(
#         max_length=35, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
#     )

from django.db import models


# class OrderItem(models.Model):
#     cart = models.ForeignKey(
#         Order,
#         related_name="order_item_set",
#         verbose_name=_('주문 아이템'),
#         on_delete=models.CASCADE,
#     )
#     product_variant = models.ForeignKey(
#         ProductVariant,
#         verbose_name=_('상품 옵션'),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#     )
#     quantity = models.PositiveIntegerField(verbose_name=_('수량'))
#     discount_price = models.PositiveIntegerField(verbose_name=_('할인 금액'))
#
#     def __str__(self):
#         return self.product_variant.product.name + '/ 옵션 : ' + self.product_variant.name
#
#     class Meta:
#         verbose_name = _("카트 아이템")
#         verbose_name_plural = _(verbose_name)
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     order_status = models.CharField(
#         choices=(
#             ('결제 완료', '결제 완료'),
#             ('배송 중', '배송 중'),
#             ('배송 완료', '배송 완료'),
#             ('취소', '취소'),
#         ),
#         default='결제 완료',
#         max_length=32,
#         verbose_name=_("주문 상태")
#     )
#     order_number = models.CharField(
#         max_length=64,
#         verbose_name=_("주문번호")
#     )
#     shipping_address = models.CharField(
#         max_length=2056,
#         verbose_name=_("배송지")
#     )
#     price = models.DecimalField(
#         max_digits=9,
#         decimal_places=2
#     )
#     quantity = models.IntegerField(default=0)
#
#     class Meta:
#         db_table = 'orders'
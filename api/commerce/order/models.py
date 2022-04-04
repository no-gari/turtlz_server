from django.utils.translation import gettext_lazy as _
from api.commerce.product.models import ProductVariant
from api.user.models import User
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField(
        choices=(
            ('결제 완료', '결제 완료'),
            ('배송 중', '배송 중'),
            ('배송 완료', '배송 완료'),
            ('취소', '취소'),
        ),
        default='결제 완료',
        max_length=32,
        verbose_name=_("주문 상태")
    )
    order_number = models.CharField(
        max_length=64,
        verbose_name=_('주문번호')
    )
    shipping_address = models.CharField(
        max_length=2056,
        verbose_name=_('배송지'),
    )
    total_price = models.PositiveIntegerField(verbose_name=_('총 주문 금액'))
    total_discount_price = models.PositiveIntegerField(verbose_name=_('총 할인 금액'))

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = _('브랜드')
        verbose_name_plural = _(verbose_name)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_('주문'),
        on_delete=models.CASCADE,
        null=True,
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        verbose_name=_('상품 옵션'),
        on_delete=models.SET_NULL,
        null=True,
    )
    quantity = models.PositiveIntegerField(verbose_name=_('수량'))
    spent_price = models.PositiveIntegerField(verbose_name=_('상품 지불 금액'))
    discount_price = models.PositiveIntegerField(verbose_name=_('상품 할인 금액'))

    def __str__(self):
        return self.product_variant.product.name + '/ 옵션 : ' + self.product_variant.name

    class Meta:
        verbose_name = _('주문 상품')
        verbose_name_plural = _(verbose_name)

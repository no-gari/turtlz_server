from django.utils.translation import gettext_lazy as _
from api.commerce.product.models import ProductVariant
from api.user.models import User
from django.db import models


class ShippingCompany(models.Model):
    slug = models.CharField(max_length=64, verbose_name=_('배송회사 슬러그'))
    name = models.CharField(max_length=64, verbose_name=_('배송회사 이름'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('배송회사')
        verbose_name_plural = _(verbose_name)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=64, verbose_name=_('주문번호'))
    shipping_address = models.CharField(
        max_length=2056,
        verbose_name=_('배송지'),
        null=True,
        blank=True,
    )
    total_price = models.PositiveIntegerField(verbose_name=_('총 주문 금액'))
    total_shipping_price = models.PositiveIntegerField(verbose_name=_('총 배송비'), null=True)
    total_discount_price = models.PositiveIntegerField(verbose_name=_('총 할인 금액'))
    is_gift = models.BooleanField(verbose_name=_('선물 여부'), default=False)
    created_at = models.DateTimeField(verbose_name=_('생성 날짜'), auto_now_add=True, null=True)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = _('주문')
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
    shipping_number = models.CharField(
        max_length=128,
        verbose_name=_("송장 번호"),
        null=True,
        blank=True,
    )
    shipping_company = models.ForeignKey(
        ShippingCompany,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('배송 회사'),
    )
    quantity = models.PositiveIntegerField(verbose_name=_('수량'))
    price = models.PositiveIntegerField(verbose_name=_('상품 금액'), null=True)
    spent_price = models.PositiveIntegerField(verbose_name=_('상품 지불 금액'))
    discount_price = models.PositiveIntegerField(verbose_name=_('상품 할인 금액'))
    able_to_write = models.BooleanField(verbose_name=_('리뷰 작성 가능 여부'), default=False)
    review_written = models.BooleanField(verbose_name=_('리뷰 작성 여부'), default=False)

    def __str__(self):
        return self.product_variant.product.name + '/ 옵션 : ' + self.product_variant.name

    class Meta:
        verbose_name = _('주문 상품')
        verbose_name_plural = _(verbose_name)


class Gift(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('주문'), on_delete=models.CASCADE)
    letter = models.TextField(verbose_name=_('편지 내용'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('생성 일시'))

    def __str__(self):
        return self.order.order_number + '(선물)'

    class Meta:
        verbose_name = _('선물하기')
        verbose_name_plural = _(verbose_name)

from django.db import models
from api.user.models import User
from api.commerce.product.models import ProductVariant
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('사용자'),
        related_name="user_cart",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('생성 일자'),
    )

    def __str__(self):
        return self.user.email + '의 장바구니'

    class Meta:
        verbose_name = _("장바구니")
        verbose_name_plural = _(verbose_name)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="cart_item_set",
        verbose_name=_('장바구니'),
        on_delete=models.CASCADE,
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        verbose_name=_('상품 옵션'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(verbose_name=_('수량'))

    def __str__(self):
        return self.product.name + ' : ' + str(self.quantity)

    class Meta:
        verbose_name = _("카트 아이템")
        verbose_name_plural = _(verbose_name)

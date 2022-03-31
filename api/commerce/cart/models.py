from django.db import models
from api.user.models import User
from api.commerce.product.models import Product
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
        verbose_name=_('장바구니'),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('상품'),
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(verbose_name=_('수량'))

    def __str__(self):
        return self.product.name + ' : ' + str(self.quantity)

    class Meta:
        verbose_name = _("카트 아이템")
        verbose_name_plural = _(verbose_name)

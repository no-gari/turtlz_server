from django.db import models
from api.user.models import User
from api.commerce.product.models import ProductVariant
from django.utils.translation import gettext_lazy as _


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('사용자'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        return self.product_variant.product.name + '/ 옵션 : ' + self.product_variant.name

    class Meta:
        verbose_name = _("카트 아이템")
        verbose_name_plural = _(verbose_name)

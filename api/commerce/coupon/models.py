from django.db import models
from api.user.models import User
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    user = models.ManyToManyField(
        User,
        through='CouponUser',
        verbose_name=_('쿠폰 사용자'),
        null=True,
        blank=True,
    )
    user_limit = models.PositiveIntegerField(verbose_name=_("쿠폰 최대 발급 개수"))
    name = models.CharField(verbose_name=_("쿠폰 이름"), help_text=_("상품 이름을 입력해주세요."), max_length=255)
    discount_price = models.IntegerField(verbose_name=_("할인 가격"),)
    expire_date = models.DateField(verbose_name=_("쿠폰 만료일자"), )

    class CouponType(models.TextChoices):
        BRAND = 'BR', _('브랜드 쿠폰')
        CART = 'CA', _('장바구니 쿠폰')

    coupon_type = models.CharField(
        max_length=2,
        choices=CouponType.choices,
        default=CouponType.BRAND,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("브랜드")
        verbose_name_plural = _(verbose_name)


# 중간 테이블
class CouponUser(models.Model):
    user = models.ForeignKey(User, verbose_name=_("유저"), on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, verbose_name=_("쿠폰"), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + self.coupon.name

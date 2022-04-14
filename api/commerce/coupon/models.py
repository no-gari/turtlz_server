from django.db import models
from api.user.models import User
from api.commerce.brand.models import Brand
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    brand = models.ForeignKey(
        Brand,
        verbose_name=_('브랜드'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    coupon_limit = models.PositiveIntegerField(
        verbose_name=_('쿠폰 최대 발급 개수'),
        help_text=_('수량 제한이 없다면 비워 주세요.'),
        null=True,
        blank=True)
    name = models.CharField(
        verbose_name=_('쿠폰 이름'),
        help_text=_('쿠폰 이름을 입력해주세요.'),
        max_length=255,
    )
    discount_price = models.IntegerField(verbose_name=_('할인 가격'))
    expire_date = models.DateField(verbose_name=_('쿠폰 만료일자'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('쿠폰')
        verbose_name_plural = _(verbose_name)


# 중간 테이블
class CouponUser(models.Model):
    user = models.ForeignKey(User, verbose_name=_('유저'), on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, verbose_name=_('쿠폰'), on_delete=models.CASCADE)
    used = models.BooleanField(default=False, verbose_name=_('사용 여부'))

    def __str__(self):
        return self.user.email + self.coupon.name

from django.db import models
from api.utils import FilenameChanger
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    name = models.CharField(verbose_name=_("쿠폰 이름"), help_text=_("상품 이름을 입력해주세요."), max_length=255)
    slug = models.CharField(verbose_name=_("쿠폰 슬러그"), max_length=255)
    has_expire_date = models.BooleanField(
        default=False,
        verbose_name=_("쿠폰 만료 유무"),
        help_text=_("체크 시 쿠폰의 만료 일자를 꼭 체크해주세요."),
    )
    expire_date = models.DateField()
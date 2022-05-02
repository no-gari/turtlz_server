from django.db import models
from api.user.models import User
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name=_('사용자'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('이름'), max_length=32, null=True)
    phone = models.CharField(verbose_name=_('휴대폰 번호'), max_length=16, null=True)
    city = models.CharField(verbose_name=_('시/도/군'), max_length=100)
    address = models.CharField(verbose_name=_('구/동'), max_length=200)
    specific_address = models.CharField(verbose_name=_('세부 주소'), max_length=200)
    post_code = models.CharField(verbose_name=_('우편번호'), max_length=10)

    def __str__(self):
        return self.user.email + '의 주소'

    class Meta:
        verbose_name = _("주소")
        verbose_name_plural = _(verbose_name)

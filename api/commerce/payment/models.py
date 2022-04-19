from django.utils.translation import gettext_lazy as _
from api.user.models import User
from django.db import models


class PaymentStatusChoices(models.TextChoices):
    READY = 'ready', '결제대기'
    PAID = 'paid', '결제완료'
    CANCELLED = 'cancelled', '결제취소'
    FAILED = 'failed', '결제실패'


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name=_('사용자'), on_delete=models.CASCADE)
    merchant_uid = models.CharField(verbose_name=_('주문 고유번호'), max_length=40)
    amount = models.PositiveIntegerField(verbose_name=_('금액'))
    status = models.CharField(verbose_name=_('주문 상태'), max_length=16, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.READY)
    created_at = models.DateTimeField(verbose_name=_('결제일시'), auto_now_add=True)

    class Meta:
        verbose_name = '결제'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.merchant_uid

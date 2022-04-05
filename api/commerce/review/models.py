from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from api.commerce.order.models import OrderItem
from api.utils import FilenameChanger
from api.user.models import User
from django.db import models


class Reviews(models.Model):
    order_item = models.ForeignKey(
        OrderItem,
        verbose_name=_('주문 아이템'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('사용자'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    rates = models.FloatField(
        verbose_name=_('리뷰 평점'),
        default=5.0,
        validators=[
            MinValueValidator(0.0), MaxValueValidator(5.0)
        ]
    )
    title = models.CharField(verbose_name=_('리뷰 제목'), max_length=128, null=True, blank=True)
    body = models.CharField(verbose_name=_('리뷰 본문'), max_length=1024, null=True, blank=True)
    image = models.ImageField(
        verbose_name=_('리뷰 이미지'),
        upload_to=FilenameChanger('review_image'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('고객 리뷰')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.email + '의 리뷰'

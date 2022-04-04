from django.db import models
from api.user.models import User
from api.utils import FilenameChanger
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    manager = models.ForeignKey(
        User,
        verbose_name=_('브랜드 담당자'),
        related_name="brand_manager",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    wish_brand = models.ManyToManyField(
        User,
        related_name='wish_brand',
        verbose_name=_('브랜드 위시리스트'),
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name=_("브랜드 이름"), help_text=_("브랜드 이름을 입력해주세요."), max_length=255)
    brand_banner = models.ImageField(
        verbose_name=_("브랜드 배너 이미지"),
        upload_to=FilenameChanger('brand_banner'),
        null=True,
        blank=True,
    )
    thumbnail_image = models.ImageField(
        verbose_name=_("브랜드 썸네일 이미지"),
        upload_to=FilenameChanger('brand_thumbnail'),
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name=_("브랜드 설명"), null=True, blank=True,)
    least_price = models.IntegerField(
        verbose_name=_("최소 주문 금액"),
        help_text=_("무료 배송을 위한 최소 주문 금액입니다."),
        null=True,
        blank=True,
    )
    shipping_price = models.IntegerField(
        verbose_name=_("배송비"),
        help_text=_("기본 배송비입니다. 도서 산간 지역 추가 배송비는 자동으로 주문서에 추가됩니다."),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("브랜드")
        verbose_name_plural = _(verbose_name)

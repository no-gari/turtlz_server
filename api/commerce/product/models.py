from django.db import models
from api.user.models import User
from api.utils import FilenameChanger
from api.commerce.brand.models import Brand
from api.commerce.category.models import Category
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(verbose_name=_("상품 이름"), help_text=_("상품 이름을 입력해주세요."), max_length=255)
    brand = models.ForeignKey(
        Brand,
        verbose_name=_('브랜드'),
        help_text=_('생성하는 상품이 해당하는 브랜드를 선택해 주세요.'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('카테고리'),
        help_text=_("가장 하위의 카테고리 하나만 골라주세요."),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    summary = models.TextField(
        verbose_name=_("상품 요약"),
        help_text=_("상품에 대한 간략한 설명을 적어주세요."),
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("상품 상세 설명"),
        help_text=_("상품에 대한 상세 설명을 적어주세요."),
        null=True,
        blank=True,
    )
    banner_img = models.ImageField(
        upload_to=FilenameChanger('product_banner_image'),
        verbose_name=_("배너 이미지"),
        help_text='배너 이미지를 올려 주세요.',
        blank=True,
        null=True,
    )
    video = models.FileField(
        upload_to=FilenameChanger('product_video1'),
        verbose_name=_("비디오 파일"),
        help_text='비디오 파일을 올려주세요.',
        null=True,
        blank=True,
    )
    org_price = models.IntegerField(verbose_name=_("정가"),)
    discount_price = models.IntegerField(verbose_name=_("할인가"),)
    is_active = models.BooleanField(
        verbose_name=_("상품 노출 여부"),
        help_text=_("체크 해제 시 상품이 어플리케이션에서 보이지 않습니다."),
        default=True,
    )
    restrict_quantity = models.BooleanField(
        verbose_name=_("상품 수량 지정하기"),
        help_text=_("체크 시 상품의 수량을 반드시 지정해주셔야 합니다. 미체크 시 수량이 무한대로 지정됩니다."),
        default=False,
    )
    created_at = models.DateTimeField(_("생성 일자"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정 일자"), auto_now=True)
    wish_product = models.ManyToManyField(
        User,
        related_name="wish_product",
        null=True,
        blank=True,
        verbose_name=_("상품 위시리스트"),
    )
    hits = models.IntegerField(verbose_name=_("조회수"), default=0)
    sold_out = models.BooleanField(
        verbose_name=_('품절 여부'),
        help_text=_('품절일 경우 체크를 해 주세요.'),
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("상품")
        verbose_name_plural = _(verbose_name)


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("상품"),
        related_name="product_variant",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("옵션 이름"),
        help_text=_("옵션 이름을 입력해주세요. ex) 색상 - 노랑, 사이즈 - S"),
    )
    restrict_quantity = models.BooleanField(
        verbose_name=_("옵션 별 수량 지정하기"),
        help_text=_("체크 시 옵션의 수량을 반드시 지정해주셔야 합니다. 미체크 시 수량이 무한대로 지정됩니다."),
        default=False,
    )
    sold_out = models.BooleanField(
        verbose_name=_('품절 여부'),
        help_text=_('품절일 경우 체크를 해 주세요.'),
        default=False,
    )
    created_at = models.DateTimeField(_("생성 일자"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정 일자"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("옵션 종류")
        verbose_name_plural = _(verbose_name)

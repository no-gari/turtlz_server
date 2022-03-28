import hashlib
from django.db import models
from api.user.models import User
from django.utils import timezone
from api.utils import FilenameChanger
from api.commerce.brand.models import Brand
from api.commerce.category.models import Category
from django.utils.translation import gettext_lazy as _

# DJANGO-SUMMERNOTE (WYSIWYG EDITOR)
from django_summernote import models as summermodel
from django_summernote.utils import get_attachment_storage, get_attachment_upload_to


class Product(models.Model):
    name = models.CharField(verbose_name=_("상품 이름"), help_text=_("상품 이름을 입력해주세요."), max_length=255)
    slug = models.CharField(verbose_name=_("상품 슬러그"), max_length=255)
    brand = models.ForeignKey(
        Brand,
        verbose_name=_('카테고리'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('카테고리'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    summary = models.TextField(
        verbose_name=_("상품 요약"),
        help_text=_("상품에 대한 간략한 설명"),
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("상품 상세 설명"),
        help_text=_("상품에 대한 상세 설명"),
        null=True,
        blank=True,
    )
    video = models.FileField(
        upload_to=FilenameChanger('product_video1'),
        verbose_name=_("비디오 파일"),
        null=True,
        blank=True,
        help_text='비디오 파일을 올려주세요.',
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
    quantity = models.IntegerField(
        verbose_name=_("상품 수량"),
        help_text=_("상품 수량을 입력해주세요. 수량을 제한하지 않으실 거라면 생략하셔도 됩니다."),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(_("생성 일자"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정 일자"), auto_now=True)
    wish_product = models.ManyToManyField(
        User,
        related_name="user_wish_product",
        null=True,
        blank=True,
        verbose_name=_("상품 위시리스트"),
    )

    def save(self, *args, **kwargs):
        hash_string = hashlib.sha1(str(timezone.now()).encode('utf-8')).hexdigest()
        self.slug = hash_string[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("상품")
        verbose_name_plural = _(verbose_name)


class ProductVariant(models.Model):
    product_option = models.ForeignKey(
        Product, related_name="product_option", on_delete=models.CASCADE
    )
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True)
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
    quantity = models.IntegerField(
        verbose_name=_("옵셜 별 수량"),
        help_text=_("옵션 수량을 입력해주세요. 수량을 제한하지 않으실 거라면 생략하셔도 됩니다."),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(_("생성 일자"), auto_now_add=True)
    updated_at = models.DateTimeField(_("수정 일자"), auto_now=True)

    def save(self, *args, **kwargs):
        hash_string = hashlib.sha1(str(timezone.now()).encode('utf-8')).hexdigest()
        self.slug = hash_string[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("옵션 종류")
        verbose_name_plural = _(verbose_name)


# SUMMERNOTE RELATED MODELS
class Files(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='매거진')
    file = models.FileField(upload_to=FilenameChanger('product_spec'), verbose_name='첨부 자료')
    org_file_name = models.CharField(max_length=255, blank=True, verbose_name='원본파일명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return str(self.product.name) + ' 의 파일'

    class Meta:
        verbose_name = '첨부 파일'
        verbose_name_plural = '첨부 파일'


class Summernote(summermodel.AbstractAttachment):
    product = summermodel.models.ForeignKey(
        Product,
        null=True,
        blank=True,
        verbose_name='상품',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='원본파일명',
    )
    file = models.FileField(
        upload_to=get_attachment_upload_to(),
        storage=get_attachment_storage(),
        unique=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '첨부 이미지'
        verbose_name_plural = '첨부 이미지'

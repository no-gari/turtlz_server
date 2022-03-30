import hashlib
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(verbose_name=_("카테고리 이름"), help_text=_("카테고리 이름을 입력해주세요."), max_length=255)
    parent = models.ForeignKey(
        'self',
        verbose_name=_('부모 카테고리'),
        help_text=_("부모 카테고리가 없는 경우 생략 해 주세요."),
        related_name='category',
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    slug = models.CharField(verbose_name=_("카테고리 슬러그"), max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        hash_string = hashlib.sha1(str(timezone.now()).encode('utf-8')).hexdigest()
        self.slug = hash_string[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("카테고리")
        verbose_name_plural = _(verbose_name)

from django.utils.translation import gettext_lazy as _
from django.db import models


class SearchKeywords(models.Model):
    keywords = models.CharField(verbose_name=_('키워드'), max_length=64, null=True, blank=True)
    order = models.IntegerField(verbose_name=_('순서'), default=0)

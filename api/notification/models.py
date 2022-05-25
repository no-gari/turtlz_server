from django.utils.translation import gettext_lazy as _
from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=512, verbose_name=_('공지사항 제목'), null=True, blank=True)
    sub_title = models.CharField(max_length=512, verbose_name=_('공지사항 부제목'), null=True, blank=True)
    url = models.URLField(verbose_name=_('본문 url 주소'))
    hits = models.PositiveIntegerField(default=0, verbose_name=_('조회수'))

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = verbose_name

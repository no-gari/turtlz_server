from django.utils.translation import gettext_lazy as _
from api.user.models import User
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


class NotificationComments(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name='공지사항 댓글')
    content = models.TextField(verbose_name='내용')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='대댓글')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return str(self.notification.title) + ' 의 댓글'

    class Meta:
        verbose_name = '공지사항 댓글'
        verbose_name_plural = verbose_name

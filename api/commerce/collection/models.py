from django.db import models


class CollectionModel(models.Model):
    _id = models.CharField(max_length=512, verbose_name='콜렉션 아이디')
    name = models.CharField(max_length=512, verbose_name='팝업 이름')
    thumbnail = models.CharField(max_length=1024, verbose_name='콜렉션 이미지 url')

    class Meta:
        verbose_name = '팝업 콜렉션'
        verbose_name_plural = verbose_name

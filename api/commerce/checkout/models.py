from django.db import models


class ShippingRequest(models.Model):
    content = models.CharField(verbose_name='요구사항', max_length=64)

    class Meta:
        verbose_name = '배송 요청사항'
        verbose_name_plural = '배송 요청사항'

    def __str__(self):
        return self.content

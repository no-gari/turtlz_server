# Generated by Django 4.0.3 on 2022-04-05 10:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0003_rename_user_limit_coupon_coupon_limit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
        migrations.AddField(
            model_name='coupon',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='쿠폰 사용자'),
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0007_alter_coupon_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_limit',
            field=models.PositiveIntegerField(blank=True, help_text='수량 제한이 없다면 비워 주세요.', null=True, verbose_name='쿠폰 최대 발급 개수'),
        ),
    ]

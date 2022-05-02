# Generated by Django 4.0.3 on 2022-05-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_orderitem_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '주문', 'verbose_name_plural': '주문'},
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성 날짜'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_gift',
            field=models.BooleanField(default=False, verbose_name='선물 여부'),
        ),
    ]

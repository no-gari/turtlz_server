# Generated by Django 4.0.3 on 2022-04-04 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0011_remove_product_quantity_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('결제 완료', '결제 완료'), ('배송 중', '배송 중'), ('배송 완료', '배송 완료'), ('취소', '취소')], default='결제 완료', max_length=32, verbose_name='주문 상태')),
                ('order_number', models.CharField(max_length=64, verbose_name='주문번호')),
                ('shipping_address', models.CharField(max_length=2056, verbose_name='배송지')),
                ('total_price', models.PositiveIntegerField(verbose_name='총 주문 금액')),
                ('total_discount_price', models.PositiveIntegerField(verbose_name='총 할인 금액')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '브랜드',
                'verbose_name_plural': '브랜드',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='수량')),
                ('spent_price', models.PositiveIntegerField(verbose_name='상품 지불 금액')),
                ('discount_price', models.PositiveIntegerField(verbose_name='상품 할인 금액')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='주문')),
                ('product_variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productvariant', verbose_name='상품 옵션')),
            ],
            options={
                'verbose_name': '주문 상품',
                'verbose_name_plural': '주문 상품',
            },
        ),
    ]

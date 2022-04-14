# Generated by Django 4.0.3 on 2022-04-07 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderitem_able_to_write_orderitem_review_written'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=64, verbose_name='배송회사 슬러그')),
                ('name', models.CharField(max_length=64, verbose_name='배송회사 아이디')),
                ('tel', models.CharField(max_length=64, verbose_name='회사 전화번호')),
            ],
            options={
                'verbose_name': '배송회사',
                'verbose_name_plural': '배송회사',
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipping_number',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='송장 번호'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=2056, null=True, verbose_name='배송지'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipping_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.shippingcompany', verbose_name='배송 회사'),
        ),
    ]
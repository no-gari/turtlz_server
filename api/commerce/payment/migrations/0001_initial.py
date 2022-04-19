# Generated by Django 4.0.3 on 2022-04-15 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_uid', models.CharField(max_length=40, verbose_name='주문 고유번호')),
                ('amount', models.PositiveIntegerField(verbose_name='금액')),
                ('status', models.CharField(choices=[('ready', '결제대기'), ('paid', '결제완료'), ('cancelled', '결제취소'), ('failed', '결제실패')], default='ready', max_length=16, verbose_name='주문 상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='결제일시')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '결제',
                'verbose_name_plural': '결제',
                'ordering': ['-created_at'],
            },
        ),
    ]

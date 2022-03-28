# Generated by Django 4.0.3 on 2022-03-28 15:43

import api.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_summernote.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='상품 이름을 입력해주세요.', max_length=255, verbose_name='상품 이름')),
                ('slug', models.CharField(max_length=255, verbose_name='상품 슬러그')),
                ('description', models.TextField(blank=True, help_text='상품에 대한 간략한 설명', null=True, verbose_name='상품 설명')),
                ('specification', models.TextField(blank=True, help_text='상품에 대한 상세 설명', null=True, verbose_name='상품 상세 설명')),
                ('org_price', models.IntegerField(verbose_name='정가')),
                ('discount_price', models.IntegerField(verbose_name='할인가')),
                ('is_active', models.BooleanField(default=True, help_text='체크 해제 시 상품이 어플리케이션에서 보이지 않습니다.', verbose_name='상품 노출 여부')),
                ('restrict_quantity', models.BooleanField(default=False, help_text='체크 시 상품의 수량을 반드시 지정해주셔야 합니다. 미체크 시 수량이 무한대로 지정됩니다.', verbose_name='상품 수량 지정하기')),
                ('quantity', models.IntegerField(blank=True, help_text='상품 수량을 입력해주세요. 수량을 제한하지 않으실 거라면 생략하셔도 됩니다.', null=True, verbose_name='상품 수량')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일자')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='category.category', verbose_name='카테고리')),
                ('wish_product', models.ManyToManyField(blank=True, null=True, related_name='user_wish_product', to=settings.AUTH_USER_MODEL, verbose_name='상품 위시리스트')),
            ],
            options={
                'verbose_name': '상품',
                'verbose_name_plural': '상품',
            },
        ),
        migrations.CreateModel(
            name='Summernote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='원본파일명')),
                ('file', models.FileField(unique=True, upload_to=django_summernote.utils.uploaded_filepath)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='상품')),
            ],
            options={
                'verbose_name': '첨부 이미지',
                'verbose_name_plural': '첨부 이미지',
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(help_text='옵션 이름을 입력해주세요. ex) 색상 - 노랑, 사이즈 - S', max_length=255, verbose_name='옵션 이름')),
                ('restrict_quantity', models.BooleanField(default=False, help_text='체크 시 옵션의 수량을 반드시 지정해주셔야 합니다. 미체크 시 수량이 무한대로 지정됩니다.', verbose_name='옵션 별 수량 지정하기')),
                ('quantity', models.IntegerField(blank=True, help_text='옵션 수량을 입력해주세요. 수량을 제한하지 않으실 거라면 생략하셔도 됩니다.', null=True, verbose_name='옵셜 별 수량')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일자')),
                ('product_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_option', to='product.product')),
            ],
            options={
                'verbose_name': '옵션 종류',
                'verbose_name_plural': '옵션 종류',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=api.utils.FilenameChanger('product_spec'), verbose_name='첨부 자료')),
                ('org_file_name', models.CharField(blank=True, max_length=255, verbose_name='원본파일명')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='매거진')),
            ],
            options={
                'verbose_name': '첨부 파일',
                'verbose_name_plural': '첨부 파일',
            },
        ),
    ]

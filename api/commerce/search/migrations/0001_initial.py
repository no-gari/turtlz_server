# Generated by Django 4.0.3 on 2022-06-19 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(blank=True, max_length=64, null=True, verbose_name='키워드')),
                ('order', models.IntegerField(default=0, verbose_name='순서')),
            ],
        ),
    ]
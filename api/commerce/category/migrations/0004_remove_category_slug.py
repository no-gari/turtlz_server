# Generated by Django 4.0.3 on 2022-04-03 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_parent_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
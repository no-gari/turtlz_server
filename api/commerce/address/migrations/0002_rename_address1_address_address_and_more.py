# Generated by Django 4.0.3 on 2022-04-04 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address1',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='district',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='addresss2',
            new_name='specific_address',
        ),
    ]

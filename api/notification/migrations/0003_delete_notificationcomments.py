# Generated by Django 4.0.3 on 2022-05-24 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NotificationComments',
        ),
    ]
# Generated by Django 3.0.14 on 2021-12-01 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20211201_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='oneDates',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='threeDates',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='twoDates',
        ),
    ]
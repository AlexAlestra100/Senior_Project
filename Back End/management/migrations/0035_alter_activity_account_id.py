# Generated by Django 3.2.12 on 2022-03-23 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0034_activity_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='account_ID',
            field=models.CharField(max_length=100),
        ),
    ]
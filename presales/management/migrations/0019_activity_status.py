# Generated by Django 3.2.12 on 2022-03-08 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0018_activity_createdbymember'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.statushistory'),
        ),
    ]
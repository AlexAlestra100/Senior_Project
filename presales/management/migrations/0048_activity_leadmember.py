# Generated by Django 3.2.12 on 2022-03-26 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0047_alter_activity_onedatetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='leadMember',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leadMember', to='management.member'),
        ),
    ]

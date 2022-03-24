# Generated by Django 3.2.12 on 2022-03-23 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0035_alter_activity_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.CharField(choices=[('Accept', 'accept'), ('Reschedule', 'reschedule'), ('Scheduled', 'scheduled'), ('Request', 'request'), ('Cancel', 'cancel'), ('Decline', 'decline'), ('Expire', 'expire')], default='Remote', max_length=50),
        ),
    ]
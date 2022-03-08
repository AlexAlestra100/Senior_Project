# Generated by Django 3.2.12 on 2022-03-08 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_auto_20220301_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                ('proficiency_ID', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.product')),
            ],
        ),
        migrations.AddField(
            model_name='presalesmember',
            name='proficiency',
            field=models.ManyToManyField(to='management.Proficiency'),
        ),
    ]

# Generated by Django 3.2.13 on 2022-10-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20220922_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='is_expired',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

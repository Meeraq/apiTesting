# Generated by Django 3.2.13 on 2022-10-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20221007_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='is_delete',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

# Generated by Django 3.2.13 on 2022-09-01 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_confirmedslotsbycoach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='fee',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='gender',
            field=models.CharField(blank=True, default='NA', max_length=200),
        ),
    ]

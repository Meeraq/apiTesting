# Generated by Django 3.2.13 on 2022-11-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20221103_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assesment',
            name='leader',
            field=models.CharField(blank=True, default='null', max_length=200),
        ),
    ]

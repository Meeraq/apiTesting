# Generated by Django 3.2.13 on 2022-07-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_daytimeslot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daytimeslot',
            name='coach',
            field=models.CharField(default='nishant', max_length=200),
        ),
    ]
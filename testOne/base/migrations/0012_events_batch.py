# Generated by Django 3.2.13 on 2022-10-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_batch_learner'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='batch',
            field=models.CharField(blank=True, default=' ', max_length=200),
        ),
    ]
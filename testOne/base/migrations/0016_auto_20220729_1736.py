# Generated by Django 3.2.13 on 2022-07-29 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_sessions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='Category',
            new_name='category',
        ),
        migrations.AddField(
            model_name='batch',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coach',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='courses',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='faculty',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='learners',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]

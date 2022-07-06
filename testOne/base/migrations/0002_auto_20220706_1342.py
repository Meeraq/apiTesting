# Generated by Django 3.2.13 on 2022-07-06 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='name',
            new_name='courseName',
        ),
        migrations.AddField(
            model_name='courses',
            name='courseCategory',
            field=models.CharField(default='null', max_length=200),
            preserve_default=False,
        ),
    ]

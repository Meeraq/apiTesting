# Generated by Django 3.2.13 on 2022-08-22 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20220822_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.profile'),
        ),
        migrations.AddField(
            model_name='learners',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.profile'),
        ),
    ]

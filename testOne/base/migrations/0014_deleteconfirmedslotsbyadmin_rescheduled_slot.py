# Generated by Django 3.2.13 on 2022-12-20 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20221220_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='deleteconfirmedslotsbyadmin',
            name='rescheduled_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.leanerconfirmedslots'),
        ),
    ]

# Generated by Django 3.2.13 on 2022-07-07 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_coursecategorys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='batch',
        ),
        migrations.AddField(
            model_name='batch',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.courses'),
        ),
    ]
# Generated by Django 3.2.13 on 2022-08-30 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20220825_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.IntegerField()),
                ('coach', models.ManyToManyField(to='base.Coach')),
            ],
        ),
        migrations.CreateModel(
            name='SlotForCoach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(blank=True, default='null', max_length=2000)),
                ('end_time', models.CharField(blank=True, default='null', max_length=2000)),
                ('date', models.DateField()),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.adminrequest')),
            ],
        ),
    ]

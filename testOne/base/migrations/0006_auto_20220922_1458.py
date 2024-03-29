# Generated by Django 3.2.13 on 2022-09-22 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20220914_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Event', max_length=200)),
                ('start_date', models.DateField(default='2022-09-09')),
                ('end_date', models.DateField(default='2022-09-09')),
                ('expire_date', models.DateField(default='2022-09-09')),
                ('count', models.IntegerField(default=0)),
                ('link', models.CharField(blank=True, default=' ', max_length=200)),
                ('_id', models.CharField(max_length=1000)),
                ('coach', models.ManyToManyField(to='base.Coach')),
            ],
        ),
        migrations.AddField(
            model_name='confirmedslotsbycoach',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='confirmedslotsbycoach',
            name='is_realeased',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='LeanerConfirmedSlots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=' ', max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.CharField(max_length=200)),
                ('organisation', models.CharField(blank=True, default=' ', max_length=200)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.events')),
                ('slot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.confirmedslotsbycoach')),
            ],
        ),
    ]

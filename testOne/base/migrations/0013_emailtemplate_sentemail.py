# Generated by Django 3.2.13 on 2023-09-18 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0016_alter_crontabschedule_timezone'),
        ('base', '0012_events_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('template_data', models.TextField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipients', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scheduled_for', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('subject', models.CharField(max_length=200)),
                ('periodic_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.periodictask')),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.emailtemplate')),
            ],
        ),
    ]

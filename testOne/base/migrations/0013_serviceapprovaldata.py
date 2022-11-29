# Generated by Django 3.2.13 on 2022-11-25 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_events_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceApprovalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.IntegerField()),
                ('fees', models.IntegerField(default='500')),
                ('total_no_of_sessions', models.IntegerField(default=0)),
                ('generated_date', models.DateField()),
                ('generate_for_month', models.CharField(blank=True, default=' ', max_length=200)),
                ('generate_for_year', models.CharField(blank=True, default=' ', max_length=200)),
                ('is_approved', models.BooleanField(blank=True, default='null')),
                ('invoice_no', models.CharField(blank=True, default=' ', max_length=200)),
                ('rejection_reason', models.CharField(blank=True, default=' ', max_length=200)),
                ('response_by_finance_date', models.DateField(blank=True, default='2022-09-09')),
                ('coach_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.coach')),
            ],
        ),
    ]
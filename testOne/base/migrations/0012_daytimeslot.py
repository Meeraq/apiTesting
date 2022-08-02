# Generated by Django 3.2.13 on 2022-07-26 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_excelfileupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='dayTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayofmock', models.CharField(choices=[('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thirsday', 'thirsday'), ('friday', 'friday'), ('saturday', 'saturday')], default='sunday', max_length=2000)),
                ('start_time_id', models.CharField(max_length=200)),
                ('end_time_id', models.CharField(max_length=200)),
                ('coach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.coach')),
            ],
        ),
    ]
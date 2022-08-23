# Generated by Django 3.2.13 on 2022-08-22 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateField(blank=True, default='2000-01-01')),
                ('Name', models.CharField(max_length=200)),
                ('Faculty', models.CharField(max_length=200)),
                ('Fees', models.CharField(max_length=200)),
                ('Frequency', models.CharField(max_length=200)),
                ('NoOfSessions', models.IntegerField()),
                ('isActive', models.BooleanField(default=False)),
                ('duration', models.IntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=2000)),
                ('dob', models.DateField(blank=True, default='2000-01-01')),
                ('gender', models.CharField(blank=True, max_length=200)),
                ('fee', models.IntegerField(blank=True, default='6000')),
                ('activeSince', models.DateField(blank=True, default='2000-01-01')),
                ('isSlotBooked', models.BooleanField(blank=True, default=False)),
                ('isActive', models.BooleanField(blank=True, default=False)),
                ('password', models.CharField(default='Nish@@nt111', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CourseCategorys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseCategoryName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DayTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('sunday', 'sunday'), ('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thirsday', 'thirsday'), ('friday', 'friday'), ('saturday', 'saturday')], default='sunday', max_length=2000)),
                ('start_time_id', models.CharField(blank=True, default='null', max_length=2000)),
                ('end_time_id', models.CharField(blank=True, default='null', max_length=2000)),
                ('week_id', models.CharField(default='1', max_length=200)),
                ('isActive', models.BooleanField(default=True)),
                ('isConfirmed', models.BooleanField(default=False)),
                ('session_id', models.CharField(default='null', max_length=200)),
                ('coach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=2000)),
                ('dob', models.DateField(blank=True, default='2000-01-01')),
                ('gender', models.CharField(blank=True, max_length=200)),
                ('fee', models.IntegerField(blank=True, default='6000')),
                ('activeSince', models.DateField(blank=True, default='2000-01-01')),
                ('isActive', models.BooleanField(blank=True, default=False)),
                ('password', models.CharField(default='Nish@@nt111', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
                ('date', models.DateField(blank=True, default='2000-01-01')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.RenameField(
            model_name='courses',
            old_name='name',
            new_name='Name',
        ),
        migrations.AddField(
            model_name='courses',
            name='course_id',
            field=models.CharField(default='0000', max_length=200),
        ),
        migrations.AddField(
            model_name='courses',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionNumber', models.IntegerField(blank=True, default='1')),
                ('start_day', models.DateField(blank=True, default='2000-01-01')),
                ('end_day', models.DateField(blank=True, default='2000-01-01')),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.batch')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('coach', 'coach'), ('admin', 'admin'), ('learner', 'learner'), ('faculty', 'faculty')], default='coach', max_length=50)),
                ('email', models.CharField(default='a@gmail.com', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Learners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Email', models.CharField(max_length=100)),
                ('PhoneNumber', models.CharField(default='7880647282', max_length=1000)),
                ('Company', models.CharField(blank=True, default='000', max_length=100)),
                ('Industry', models.CharField(blank=True, default='000', max_length=100)),
                ('Designation', models.CharField(blank=True, default='000', max_length=100)),
                ('DOB', models.DateField(blank=True, default='2000-01-01')),
                ('Gender', models.CharField(blank=True, default='male', max_length=100)),
                ('isActive', models.BooleanField(default=False)),
                ('password', models.CharField(default='Nish@@nt111', max_length=50)),
                ('Batch', models.ManyToManyField(to='base.Batch')),
                ('Course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.courses')),
            ],
        ),
        migrations.CreateModel(
            name='LearnerdayTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('isConfirmed', models.BooleanField(default=False)),
                ('day', models.CharField(default='sunday', max_length=200)),
                ('coach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.coach')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.courses')),
                ('learner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.learners')),
                ('slot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.daytimeslot')),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.courses'),
        ),
        migrations.AddField(
            model_name='courses',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.coursecategorys'),
        ),
    ]
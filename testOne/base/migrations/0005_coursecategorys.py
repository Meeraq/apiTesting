# Generated by Django 3.2.13 on 2022-07-07 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20220707_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategorys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseCategoryName', models.CharField(max_length=200)),
            ],
        ),
    ]

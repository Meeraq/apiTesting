# Generated by Django 3.2.13 on 2022-07-25 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20220720_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file_upload', models.FileField(upload_to='excel')),
            ],
        ),
    ]
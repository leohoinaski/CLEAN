# Generated by Django 4.2.6 on 2023-11-06 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CLEANcalibration', '0005_alter_cleancalibrationnewdevicemodel_clean01_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleancalibrationnewdevicemodel',
            name='outzip',
            field=models.FileField(blank=True, null=True, upload_to='calibration'),
        ),
    ]

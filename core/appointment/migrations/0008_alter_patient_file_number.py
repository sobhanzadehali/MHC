# Generated by Django 4.2.20 on 2025-03-20 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0007_appointment_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='file_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='file number'),
        ),
    ]

# Generated by Django 4.2.20 on 2025-04-08 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0009_appointment_is_canceled'),
        ('payment', '0004_alter_appointmentcost_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointment.patient', verbose_name='patient')),
            ],
            options={
                'verbose_name': 'payment history',
                'verbose_name_plural': 'payment histories',
            },
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-01 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_booking_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='service',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='vendor',
        ),
    ]

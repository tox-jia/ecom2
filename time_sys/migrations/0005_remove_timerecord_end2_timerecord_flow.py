# Generated by Django 5.2 on 2025-06-16 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_sys', '0004_timerecord_duration_timerecord_end_timerecord_end2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timerecord',
            name='end2',
        ),
        migrations.AddField(
            model_name='timerecord',
            name='flow',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

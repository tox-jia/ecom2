# Generated by Django 5.2 on 2025-07-04 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_sys', '0013_timereport_day_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timereport',
            old_name='day_data',
            new_name='day_pr_data',
        ),
    ]

# Generated by Django 5.2 on 2025-07-05 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_sys', '0015_healthmedicinetag_healthrecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthmedicinetag',
            old_name='tag',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='healthmedicinetag',
            name='type',
        ),
    ]

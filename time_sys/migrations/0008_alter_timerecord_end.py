# Generated by Django 5.2 on 2025-06-19 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_sys', '0007_remove_timerecord_end2_alter_timerecord_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timerecord',
            name='end',
            field=models.DateTimeField(),
        ),
    ]

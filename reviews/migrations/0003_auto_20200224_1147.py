# Generated by Django 2.2.5 on 2020-02-24 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20200224_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Check_in',
            new_name='check_in',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='Communication',
            new_name='communication',
        ),
    ]

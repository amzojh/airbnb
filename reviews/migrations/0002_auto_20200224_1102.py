# Generated by Django 2.2.5 on 2020-02-24 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Cleanliness',
            new_name='cleanliness',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='Location',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='Value',
            new_name='value',
        ),
    ]
# Generated by Django 2.2.6 on 2020-05-22 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20200522_0656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='costs',
            new_name='price',
        ),
    ]

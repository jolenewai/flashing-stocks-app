# Generated by Django 2.2.6 on 2020-05-26 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_download'),
    ]

    operations = [
        migrations.RenameField(
            model_name='download',
            old_name='date_purchased',
            new_name='date',
        ),
    ]

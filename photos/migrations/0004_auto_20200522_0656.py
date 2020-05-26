# Generated by Django 2.2.6 on 2020-05-22 06:56

from django.db import migrations, models
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0006_auto_20200522_0459'),
        ('photos', '0003_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='title',
            new_name='caption',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='url',
        ),
        migrations.AddField(
            model_name='photo',
            name='album',
            field=models.ManyToManyField(to='photographers.Album'),
        ),
        migrations.AddField(
            model_name='photo',
            name='image',
            field=pyuploadcare.dj.models.ImageField(blank=True),
        ),
    ]
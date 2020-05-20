# Generated by Django 2.2.6 on 2020-05-20 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0002_album'),
        ('photos', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('costs', models.FloatField()),
                ('category', models.ManyToManyField(to='photos.Category')),
                ('owner', models.ForeignKey(on_delete='CASCADE', to='photographers.Photographer')),
                ('tags', models.ManyToManyField(to='photos.Tag')),
            ],
        ),
    ]

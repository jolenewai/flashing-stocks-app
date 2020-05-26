# Generated by Django 2.2.6 on 2020-05-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0009_auto_20200526_1251'),
        ('customers', '0004_remove_customer_join_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchased', models.DateTimeField(auto_now_add=True)),
                ('size', models.CharField(max_length=10)),
                ('image', models.ForeignKey(on_delete='CASCADE', to='photos.Photo')),
                ('user', models.ForeignKey(on_delete='CASCADE', to='customers.Customer')),
            ],
        ),
    ]

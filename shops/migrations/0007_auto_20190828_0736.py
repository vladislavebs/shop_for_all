# Generated by Django 2.2.4 on 2019-08-28 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190826_2232'),
        ('shops', '0006_auto_20190827_2359'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='storeproduct',
            unique_together={('store', 'product')},
        ),
    ]

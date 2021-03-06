# Generated by Django 2.2.4 on 2019-08-27 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20190826_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'products'), ('model', 'product')), models.Q(('app_label', 'shops'), ('model', 'storecategory')), models.Q(('app_label', 'shops'), ('model', 'storeproduct')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='price', to='contenttypes.ContentType'),
        ),
    ]

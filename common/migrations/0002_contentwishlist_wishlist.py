# Generated by Django 2.2.4 on 2019-08-24 14:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import shop_for_all.helpers.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.SlugField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(shop_for_all.helpers.models.BasicModel,),
        ),
        migrations.CreateModel(
            name='ContentWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(('app_label', 'products'), ('model', 'product')), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='common.WishList')),
            ],
        ),
    ]

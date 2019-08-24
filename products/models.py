from django.db import models

from shop_for_all.helpers.models import BasicModel


MAX_LENGTH = 255


class Category(models.Model, BasicModel):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    codename = models.SlugField(max_length=MAX_LENGTH, unique=True)


class Product(models.Model, BasicModel):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    codename = models.SlugField(max_length=MAX_LENGTH, unique=True)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        to=Category, related_name="products", on_delete=models.DO_NOTHING
    )

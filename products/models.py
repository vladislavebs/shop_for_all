from django.db import models

from shop_for_all.constants.models import MAX_LENGTH
from shop_for_all.helpers.models import BasicModel


class Category(BasicModel):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    codename = models.SlugField(max_length=MAX_LENGTH, blank=True, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(BasicModel):
    name = models.CharField(max_length=MAX_LENGTH)
    codename = models.SlugField(max_length=MAX_LENGTH, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        to=Category, related_name="products", on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        unique_together = ("name", "category")

    def __str__(self):
        return self.name

from django.db import models

from products import models as products_model
from shop_for_all.constants.models import MAX_LENGTH
from shop_for_all.helpers.django import USER_MODEL
from shop_for_all.helpers.models import BasicModel


class Store(BasicModel):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    codename = models.SlugField(max_length=MAX_LENGTH, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(
        to=products_model.Product, through="StoreProduct", related_name="stores"
    )
    categories = models.ManyToManyField(
        to=products_model.Category, through="StoreCategory", related_name="stores"
    )
    user = models.OneToOneField(
        to=USER_MODEL, related_name="user", on_delete=models.CASCADE
    )


class StoreProduct(models.Model):
    store = models.ForeignKey(
        to=Store, related_name="store_products", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=products_model.Product,
        related_name="product_stores",
        on_delete=models.CASCADE,
    )


class StoreCategory(models.Model):
    store = models.ForeignKey(
        to=Store, related_name="store_categories", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        to=products_model.Category,
        related_name="category_stores",
        on_delete=models.CASCADE,
    )

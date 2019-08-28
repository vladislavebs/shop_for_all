from django.db import models

from common.models import PRICES_RELATION, Price
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
        to=USER_MODEL, related_name="store", on_delete=models.CASCADE
    )

    def add_product(
        self, product: products_model.Product, basic_price: int, prices=None
    ):
        store_product, created = StoreProduct.objects.get_or_create(
            store=self, product=product
        )

        if created:
            product_prices = [
                Price(price=basic_price, content_object=store_product),
                *[
                    Price(
                        price=price["price"],
                        start_date=price.get("start_date"),
                        end_date=price.get("end_date"),
                        content_object=store_product,
                    )
                    for price in prices or []
                ],
            ]

            Price.objects.bulk_create(product_prices)

        return store_product


class StoreProduct(models.Model):
    store = models.ForeignKey(
        to=Store, related_name="store_product", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=products_model.Product,
        related_name="product_store",
        on_delete=models.CASCADE,
    )

    prices = PRICES_RELATION

    class Meta:
        unique_together = ("store", "product")

    @property
    def price(self):
        return 0


class StoreCategory(models.Model):
    store = models.ForeignKey(
        to=Store, related_name="store_category", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        to=products_model.Category,
        related_name="category_store",
        on_delete=models.CASCADE,
    )

    prices = PRICES_RELATION

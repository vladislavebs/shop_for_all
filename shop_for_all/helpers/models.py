import time
from functools import reduce

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import class_prepared
from django.dispatch import receiver
from slugify import slugify

from shop_for_all.helpers.methods import hasattrs


def format_foreign_key_limit(foreign_limit, limit):
    app, model = limit
    q = models.Q(app_label=app, model=model)

    if not foreign_limit:
        return q

    return foreign_limit | q


@receiver(class_prepared)
def add_field(sender, *_, **__):
    if GenericModel in sender.__bases__:
        limit_models = reduce(format_foreign_key_limit, sender.limit_models, None)

        models.ForeignKey(
            to=ContentType,
            on_delete=sender.generic_on_delete,
            limit_choices_to=limit_models,
        ).contribute_to_class(sender, "content_type")

        models.PositiveIntegerField().contribute_to_class(sender, "object_id")


class DeleteStatusQuerySet(models.QuerySet):
    def delete(self):
        delete_status = getattr(self, "delete_status", None)

        if delete_status:
            self.update(status=delete_status)
            return 0, {}

        return super(DeleteStatusQuerySet, self).delete()


class BasicModel(models.Model):
    objects = DeleteStatusQuerySet.as_manager()
    delete_status = None

    class Meta:
        abstract = True

    def delete(self, make_delete=False, *args, **kwargs):
        if make_delete or not hasattrs(self, "status", "delete_status"):
            return super(BasicModel, self).delete(*args, **kwargs)

        self.status = self.delete_status
        self.save()

    def save(self, *args, **kwargs):
        if hasattrs(self, "name", "codename") and not self.codename:
            # noinspection PyUnresolvedReferences
            self.codename = slugify(
                text=self.name,
                max_length=250,
                word_boundary=True,
                save_order=True,
                separator="_",
            )

            if self.__class__.objects.filter(codename=self.codename).exists():
                self.codename = f"{self.codename}_{int(time.time())}"

        super(BasicModel, self).save(*args, **kwargs)


class GenericModel(models.Model):
    generic_to = None
    generic_on_delete = None
    limit_models = None
    content_type = None

    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True

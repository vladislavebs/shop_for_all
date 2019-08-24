from django.db import models


class DeleteStatusQuerySet(models.QuerySet):
    def delete(self):
        delete_status = getattr(self, "delete_status", None)

        if delete_status:
            self.update(status=delete_status)
            return 0, {}

        return super(DeleteStatusQuerySet, self).delete()


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class BasicModel:
    objects = DeleteStatusQuerySet.as_manager()
    delete_status = None

    def delete(self, make_delete=False, *args, **kwargs):
        if make_delete or not hasattr(self, "delete_status"):
            return super(BasicModel, self).delete(*args, **kwargs)

        self.status = self.delete_status
        self.save()

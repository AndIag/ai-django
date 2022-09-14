import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class EditableQuerySet(QuerySet):
    """Avoid models in QuerySet (self) to be updated/deleted if no edition is allowed in any of the given instances"""

    def update(self, **kwargs):
        if self.exclude(self.model.condition).exists():
            raise ValueError(_('Trying to update non editable instances'))
        return super(EditableQuerySet, self).update(**kwargs)

    def delete(self):
        if self.exclude(self.model.condition).exists():
            raise ValueError(_('Trying to remove non editable instances'))
        return super(EditableQuerySet, self).delete()

    def hard_update(self, **kwargs):
        """Force model update even if non-editable"""
        return super(EditableQuerySet, self).update(**kwargs)

    def hard_delete(self):
        """Force model deletion even if non-editable"""
        return super(EditableQuerySet, self).delete()


class EditableManager(models.Manager):
    def get_queryset(self):
        return EditableQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class EditableMixin(object):
    """
    Add (not implemented) 'is_editable' property to a model used to
    control when a model instance can be edited or removed.

    WARNING: Mixin should be put first in inheritance order
    """

    objects = EditableManager()

    @property
    def is_editable(self):
        raise NotImplementedError

    @property
    def condition(self):
        raise NotImplementedError

    def save(self, force_insert=False, force_update=False):
        """
        :param force_insert: avoid 'is_editable' check
        :param force_update: avoid 'is_editable' check
        """
        if not force_insert and not force_update and not self.is_editable:
            raise ValidationError({"non_field_errors": _("Non editable: %(name)s" % {"name": self.__str__()})})

    def delete(self):
        if not self.is_editable:
            raise ValidationError({"non_field_errors": _("Non editable: %(name)s" % {"name": self.__str__()})})

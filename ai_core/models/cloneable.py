import logging
from copy import copy

from django.db import models

logger = logging.getLogger(__name__)


class CloneableModel(models.Model):
    cloned_from = models.ForeignKey(
        to='self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="clones",
        related_query_name="clone"
    )

    @staticmethod
    def _replace(duplicate, fields):
        """Will replace the "fields" in the given instance."""
        if fields:
            for attname, value in fields.items():
                setattr(duplicate, attname, value)

    def _copy(self):
        if not self.pk:
            raise ValueError(self)
        return copy(self)

    def _prepare_clone(self, duplicate, exclude=None):
        """
        Prepare the object for being cloned setting default values to excluded fields
        and updating values for 'auto_now' and 'auto_now_add' dates.
        """

        def unset_pk_and_parent_relation(cls):
            """
            Setting pk to None tricks Django into not trying to overwrite the old object
            """
            setattr(duplicate, cls._meta.pk.attname, None)
            for parent, f in cls._meta.parents.items():
                unset_pk_and_parent_relation(parent)

        unset_pk_and_parent_relation(duplicate.__class__)

        for field in self._meta.fields:
            # Assign default value to excluded fields.
            if exclude and field.name in exclude:
                setattr(duplicate, field.attname, field.get_default())
            # Update time fields if 'auto_now' or 'auto_now_add'.
            if isinstance(field, (models.DateField, models.TimeField, models.DateTimeField)):
                if field.auto_now or field.auto_now_add:
                    field.pre_save(duplicate, True)

    # noinspection PyProtectedMember
    def __clone_fk(self, duplicate, exclude=None):
        """Clone all related ForeignKey"""
        for field in self._meta.related_objects:
            if field.one_to_many and hasattr(field, 'clone'):
                # Check relation is not being excluded
                if any(field.related_model._meta.db_table == model._meta.db_table for model in exclude):
                    # Accessing _meta and compare db_table is not the best option but no wonder how to do it otherwise.
                    continue
                for foreign in list(getattr(self, field.related_name or '{}_set'.format(field.name)).all()):
                    foreign.clone(attrs={field.remote_field.attname: duplicate.id}, exclude=exclude)

    # noinspection PyProtectedMember
    def __clone_m2m(self, duplicate, exclude=None):
        """Clone Many2Many relations (will only clone auto_created through model)."""
        for field in self._meta.many_to_many:
            if field.many_to_many and hasattr(field, 'clone'):
                # Check relation is not being excluded
                if any(field.related_model._meta.db_table == model._meta.db_table for model in exclude):
                    # Accessing _meta and compare db_table is not the best option but no wonder how to do it otherwise.
                    continue
                if field.remote_field.through._meta.auto_created:
                    setattr(duplicate, field.attname, getattr(self, field.attname).all())

    def clone(self, attrs=None, exclude=None):
        duplicate = self._copy()
        self._prepare_clone(duplicate, exclude=exclude)
        self._replace(duplicate, fields=attrs)

        # Force insert in order to avoid Django to update current instance
        # https://docs.djangoproject.com/en/2.1/ref/models/instances/#forcing-an-insert-or-update
        duplicate.cloned_from = self
        duplicate.save(force_insert=True)

        # Fix dependencies
        self.__clone_fk(duplicate, exclude=exclude)
        self.__clone_m2m(duplicate, exclude=exclude)

        return duplicate

    class Meta:
        abstract = True

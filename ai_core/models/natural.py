from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class KeyManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(key=name)


class KeyModel(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\_]+$',
                message=_("Key must be uppercase words separated by '_'"),
                code='invalid_key'
            )
        ]
    )

    class Key:
        @classmethod
        def members(cls):
            return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]

    def __str__(self):
        return self.key

    def natural_key(self):
        return self.key,

    class Meta:
        abstract = True

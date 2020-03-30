from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from rest_framework.relations import RelatedField


class NaturalKeyRelatedField(RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid key "{key_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected key value, received {data_type}.'),
    }

    def __init__(self, **kwargs):
        self.key_field = kwargs.pop('key_field', None)
        super(NaturalKeyRelatedField, self).__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_internal_value(self, data):
        if self.key_field is not None:
            data = self.key_field.to_internal_value(data)
        try:
            return self.get_queryset().get(key=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', key_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        if self.key_field is not None:
            return self.key_field.to_representation(value.key)
        return value.key

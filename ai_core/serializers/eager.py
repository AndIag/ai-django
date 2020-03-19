from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import empty


class EagerSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, eager=True, **kwargs):
        if eager and instance is not None and isinstance(instance, QuerySet):
            instance = self.setup_eager_loading(instance)
        super(EagerSerializer, self).__init__(instance=instance, data=data, **kwargs)

    @staticmethod
    def setup_eager_loading(queryset: QuerySet):
        raise NotImplementedError

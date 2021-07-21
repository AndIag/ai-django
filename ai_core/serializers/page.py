from django.conf import settings
from rest_framework import serializers

DEFAULT_PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE', 30)


class PaginatedFilterSerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=0, default=DEFAULT_PAGE_SIZE, allow_null=False)
    offset = serializers.IntegerField(min_value=0, default=0, allow_null=False)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

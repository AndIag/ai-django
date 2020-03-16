from django.utils.encoding import force_text
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('{model} {value} not found')
    default_code = 'not_found'

    def __init__(self, model, value):
        detail = force_text(self.default_detail).format(model=model, value=value)
        super(NotFound, self).__init__(detail)


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'conflict'
